from datetime import datetime, timedelta

from flask_restful import Resource, reqparse
from loguru import logger

from utils.oauth import USER_AUTH, GW_AUTH, g
from config import SESSION, VOLTAGE
from .model import MeterData
from ..sensor.model import Sensor


class MeterDataResource(Resource):
    """Get and Upload Meter Data"""

    def __init__(self):
        # Upload Data
        self._set_post_parser()

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
