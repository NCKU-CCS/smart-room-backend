from datetime import datetime, timedelta

from flask_restful import Resource, reqparse
from loguru import logger

# from sqlalchemy import cast, TIMESTAMP, func, INTEGER, case, DECIMAL
from sqlalchemy import TIMESTAMP, func, cast, DECIMAL
from sqlalchemy.sql.functions import concat
from sqlalchemy.dialects.postgresql import INTERVAL

from utils.oauth import USER_AUTH, GW_AUTH, g
from config import db, VOLTAGE
from .model import MeterData
from ..sensor.model import Sensor
from ..sensor_data.model import SensorData


class MeterDataResource(Resource):
    """Get and Upload Meter Data"""

    def __init__(self):
        # Get Data
        self._set_get_parser()
        self.args: reqparse.Namespace
        # Upload Data
        self._set_post_parser()

    def _set_get_parser(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("start_time", type=datetime.fromisoformat, required=True, location="values")
        self.get_parser.add_argument("end_time", type=datetime.fromisoformat, required=True, location="values")
        self.get_parser.add_argument("interval", type=str, choices=["hour", "day"], required=True, location="values")

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        data_arguments = ["voltage", "current", "power", "total_current"]
        for arg in data_arguments:
            self.post_parser.add_argument(
                arg, type=float, required=True, location="json", help=f"Upload Data: {arg} is required"
            )
        self.post_parser.add_argument(
            "sensor", type=str, required=True, location="json", help="Upload Data: sensor is required"
        )

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get Meter Data"""
        logger.info(f"[Get Meter Data Request]\n User: {g.account}")
        self.args = self.get_parser.parse_args()
        # Get Sensors
        sensors: list = (
            db.session.query(Sensor.name, Sensor.room, Sensor.device_type)
            .filter(Sensor.device_type.in_(["CT", "thermo_sensor"]))
            .all()
        )
        room_sensor: dict = {"overview": {"thermo_sensor": list(), "CT": list()}}
        for sensor in sensors:
            if sensor.room not in room_sensor:
                room_sensor[sensor.room] = {"thermo_sensor": list(), "CT": list()}
            if sensor.device_type in room_sensor[sensor.room]:
                room_sensor[sensor.room][sensor.device_type].append(sensor.name)
            else:
                room_sensor[sensor.room][sensor.device_type] = [sensor.name]
            room_sensor["overview"][sensor.device_type].append(sensor.name)
        # Create Data
        data: dict = dict()
        for room in room_sensor:
            logger.info(f"[Get Data] {room}")
            data[room] = self.get_room_data(room_sensor[room])
        return data

    # pylint: enable=R0201

    def get_room_data(self, room_sensor: dict):
        if self.args["interval"] == "hour":
            power = func.round(cast(func.avg(MeterData.current) * VOLTAGE, DECIMAL), 2).label("power")
            time_format = "YYYY-MM-DD HH24:00:00"
        else:
            power = func.round(cast(func.avg(MeterData.current) * VOLTAGE * 24, DECIMAL), 2).label("power")
            time_format = "YYYY-MM-DD"
        # Get Meter Data
        combined_data = {
            "power": self.get_meter_data(self.simplify_date(MeterData.created, time_format), power, room_sensor["CT"]),
            "temp": self.get_temp_data(
                self.simplify_date(SensorData.created, time_format), room_sensor["thermo_sensor"]
            ),
        }
        return combined_data

    def get_meter_data(self, date, power, ct_sensors: list):
        criteria = [
            MeterData.created.between(self.args["start_time"], self.args["end_time"]),
            MeterData.sensor.in_(ct_sensors),
        ]
        # CT Data
        meter_ct = (
            db.session.query(MeterData.sensor, date, power)
            .filter(*criteria)
            .group_by(date, MeterData.sensor)
            .subquery()
        )
        # Group Data By Date
        meter_sum = (
            db.session.query(func.sum(meter_ct.c.power).label("power"), meter_ct.c.datetime.label("datetime"))
            .group_by(meter_ct.c.datetime)
            .order_by(meter_ct.c.datetime)
            .all()
        )
        meter_data = {meter.datetime.isoformat(): float(meter.power) for meter in meter_sum}
        return meter_data

    def get_temp_data(self, date, temp_sensors: list):
        criteria = [
            SensorData.created.between(self.args["start_time"], self.args["end_time"]),
            SensorData.sensor.in_(temp_sensors),
        ]
        # Thermo Sensor Data
        sensor_thermo = (
            db.session.query(func.avg(SensorData.temperature).label("temperature"), date)
            .filter(*criteria)
            .group_by(date)
            .all()
        )
        thermo_data = {thermo.datetime.isoformat(): float(thermo.temperature) for thermo in sensor_thermo}
        return thermo_data

    @staticmethod
    def simplify_date(column: db.column, time_format: str):
        date_tz = cast(column + func.cast(concat(8, ' HOURS'), INTERVAL), TIMESTAMP)
        date = cast(func.to_char(date_tz, time_format), TIMESTAMP).label('datetime')
        return date

    # pylint: disable=R0201
    @GW_AUTH.login_required
    def post(self):
        """Upload Meter Data"""
        logger.info(f"[Upload Data Request]\n GW: {g.gateway_name}")
        data = self.post_parser.parse_args()
        data["gateway"] = g.gateway_name
        if MeterData(**data).add():
            return {"message": "Success"}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201


class MeterDataOverview(Resource):
    """Get Meter Data Overview"""

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get Meter Data Overview"""
        logger.info(f"[Get Meter Data Overview Request]\n User: {g.account}")
        return self.get_overview()

    # pylint: enable=R0201

    @staticmethod
    def get_overview():
        """Get latest power consumption data"""
        ct_sensors = Sensor.query.filter(Sensor.device_type == "CT").all()
        ct_sensor_name = [sensor.name for sensor in ct_sensors]
        ct_room: dict = {sensor.name: sensor.room for sensor in ct_sensors}
        power = (MeterData.current * VOLTAGE).label("power")
        criteria = [MeterData.sensor.in_(ct_sensor_name), MeterData.created >= datetime.utcnow() - timedelta(minutes=5)]
        ct_data = (
            db.session.query(MeterData.sensor, power)
            .filter(*criteria)
            .order_by(MeterData.sensor, MeterData.created.desc())
            .distinct(MeterData.sensor)
            .all()
        )
        power_overview: dict = {"total": 0.0, "room": dict()}
        for data in ct_data:
            power_overview["total"] += data.power
            if ct_room[data.sensor] in power_overview["room"]:
                power_overview["room"][ct_room[data.sensor]] += data.power
            else:
                power_overview["room"][ct_room[data.sensor]] = data.power
        return power_overview
