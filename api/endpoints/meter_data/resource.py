from datetime import datetime, timedelta
from typing import Set, Dict

from flask_restful import Resource, reqparse
from loguru import logger

from sqlalchemy import TIMESTAMP, func, cast, DECIMAL
from sqlalchemy.sql.functions import concat
from sqlalchemy.dialects.postgresql import INTERVAL

from utils.oauth import USER_AUTH, GW_AUTH, g
from config import SESSION, VOLTAGE, TZ_OFFSET, OUTDOOR_THERMO_SENSORS
from database.migrations.models import Sensor, SensorData, MeterData


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
        data_arguments = ["voltage", "current", "power", "total_current", "total_consumption"]
        for arg in data_arguments:
            self.post_parser.add_argument(
                arg, type=float, required=False, location="json", help=f"Upload Data: {arg} is required"
            )
        # TODO: Set required to True and remove total_current
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
            SESSION.query(Sensor.name, Sensor.room, Sensor.device_type)
            .filter(Sensor.device_type.in_(["CT", "thermo_sensor"]))
            .all()
        )
        rooms: Set[str] = {sensor.room for sensor in sensors} | {"overview"}
        try:
            sensor_info = {room: {"thermo_sensor": [], "CT": []} for room in rooms}
            sensor_info["overview"] = {
                "thermo_sensor": OUTDOOR_THERMO_SENSORS,
                "CT": [sensor.name for sensor in sensors if sensor.device_type == "CT"],
            }
            for sensor in sensors:
                if sensor.room in sensor_info and sensor.device_type in sensor_info[sensor.room]:
                    sensor_info[sensor.room][sensor.device_type].append(sensor.name)
            return {room: self.get_room_data(sensor_info[room]) for room in rooms}
        except Exception as err:
            logger.error(err)
            return {"message": "error"}, 400

    # pylint: enable=R0201

    def get_room_data(self, room_sensor: Dict[str, list]) -> Dict[str, dict]:
        """Get Data of One Room

        Args:
            room_sensor (Dict[str, list]): include list of `CT` and `thermo_sensor`

        Returns:
            Dict[str, dict]: include `power` and `temp`, Dict[datetime.isoformat, float] in fields
        """
        # Get Meter Data
        combined_data = {
            "power": self.get_meter_data(room_sensor["CT"]),
            "temp": self.get_temp_data(room_sensor["thermo_sensor"]),
        }
        return combined_data

    def get_meter_data(self, ct_sensors: list) -> Dict[datetime.isoformat, float]:
        """Get Meter Data with Specific CT Sensors

        Args:
            ct_sensors (list): CT sensors

        Returns:
            Dict[datetime.isoformat, float]: historical power consumption data
        """
        if self.args["interval"] == "hour":
            power = func.round(cast(func.avg(MeterData.current) * VOLTAGE, DECIMAL), 2).label("power")
            time_format = "YYYY-MM-DD HH24:00:00"
        elif self.args["interval"] == "day":
            power = func.round(cast(func.avg(MeterData.current) * VOLTAGE * 24, DECIMAL), 2).label("power")
            time_format = "YYYY-MM-DD 00:00:00"
        else:
            raise Exception(f"Invalid interval: {self.args['interval']}")
        date = self.simplify_date(MeterData.created, time_format)
        criteria = [
            MeterData.created.between(self.args["start_time"], self.args["end_time"]),
            MeterData.sensor.in_(ct_sensors),
        ]
        # CT Data
        meter_ct = (
            SESSION.query(MeterData.sensor, date, power).filter(*criteria).group_by(date, MeterData.sensor).subquery()
        )
        # Group Data By Date
        meter_sum = (
            SESSION.query(func.sum(meter_ct.c.power).label("power"), meter_ct.c.datetime.label("datetime"))
            .group_by(meter_ct.c.datetime)
            .order_by(meter_ct.c.datetime)
            .all()
        )
        meter_data = {meter.datetime.isoformat(): float(meter.power) for meter in meter_sum}
        return meter_data

    def get_temp_data(self, temp_sensors: list) -> Dict[datetime.isoformat, float]:
        """Get Temperature Data with Specific Thermo Sensors

        Args:
            temp_sensors (list): Thermo Sensors

        Returns:
            Dict[datetime.isoformat, float]: historical temperature data
        """
        if self.args["interval"] == "hour":
            time_format = "YYYY-MM-DD HH24:00:00"
        elif self.args["interval"] == "day":
            time_format = "YYYY-MM-DD 00:00:00"
        else:
            raise Exception(f"Invalid interval: {self.args['interval']}")
        date = self.simplify_date(SensorData.created, time_format)
        criteria = [
            SensorData.created.between(self.args["start_time"], self.args["end_time"]),
            SensorData.sensor.in_(temp_sensors),
        ]
        # Thermo Sensor Data
        sensor_thermo = (
            # fmt: off
            SESSION.query(func.round(
                cast(func.avg(SensorData.temperature), DECIMAL), 2
            ).label("temperature"), date)
            .filter(*criteria)
            .group_by(date)
            .all()
            # fmt: on
        )
        thermo_data = {thermo.datetime.isoformat(): float(thermo.temperature) for thermo in sensor_thermo}
        return thermo_data

    @staticmethod
    def simplify_date(column, time_format: str):
        date_tz = cast(column + func.cast(concat(TZ_OFFSET, " HOURS"), INTERVAL), TIMESTAMP)
        date = cast(func.to_char(date_tz, time_format), TIMESTAMP).label("datetime")
        return date

    # pylint: disable=R0201
    @GW_AUTH.login_required
    def post(self):
        """Upload Meter Data"""
        logger.info(f"[Upload Data Request]\n GW: {g.gateway_name}")
        data = self.post_parser.parse_args()
        data["gateway"] = g.gateway_name
        # TODO: remove this if-else statement
        if data["total_current"] and not data["total_consumption"]:
            data["total_consumption"] = data.pop("total_current")
        logger.debug(data)
        if MeterData(**data).add(SESSION):
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
        ct_sensors = SESSION.query(Sensor).filter(Sensor.device_type == "CT").all()
        ct_sensor_name = [sensor.name for sensor in ct_sensors]
        ct_room: dict = {sensor.name: sensor.room for sensor in ct_sensors}
        power = (MeterData.current * VOLTAGE).label("power")
        criteria = [MeterData.sensor.in_(ct_sensor_name), MeterData.created >= datetime.utcnow() - timedelta(minutes=5)]
        ct_data = (
            SESSION.query(MeterData.sensor, power)
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
