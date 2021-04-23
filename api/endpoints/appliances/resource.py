from flask_restful import Resource, reqparse
from loguru import logger

from utils.oauth import USER_AUTH, g
from ..sensor.model import Sensor
from ..sensor_data.model import SensorData
from ..device.model import Device
from ..control.model import ControlRecord


class AppliancesResource(Resource):
    """Appliances Management"""

    def __init__(self):
        # Get Appliances
        self._set_get_parser()

    def _set_get_parser(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("room", type=str, required=False, location="values")
        self.get_parser.add_argument("location", type=str, required=False, location="values")

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get Appliances"""
        args = self.get_parser.parse_args()
        logger.info(f"[Get Appliances] User: {g.account}")
        criteria_sensor: list = [Sensor.device_type == "thermo_sensor"]
        criteria_device: list = list()
        for argument in args:
            if args[argument]:
                criteria_sensor.append(getattr(Sensor, argument) == args[argument])
                criteria_device.append(getattr(Device, argument) == args[argument])
        appliances_status = []
        sensors = Sensor.query.filter(*criteria_sensor).all()
        for sensor in sensors:
            appliances_status.append(self.get_latest_sensor_data(sensor.device_type, sensor.name, sensor.room))
        devices = Device.query.filter(*criteria_device).all()
        for device in devices:
            appliances_status.append(self.get_latest_sensor_data("ac", device.name, device.room))
        return appliances_status

    # pylint: enable=R0201

    @staticmethod
    def get_latest_sensor_data(device_type: str, name: str, location: str) -> dict:
        if device_type == "thermo_sensor":
            latest_data: SensorData = (
                SensorData.query.filter(SensorData.sensor == name).order_by(SensorData.created.desc()).first()
            )
            if latest_data:
                data = {"temperature": latest_data.temperature, "humidity": latest_data.humidity}
            else:
                data = {"temperature": None, "humidity": None}
        elif device_type == "ac":
            latest_data: ControlRecord = (
                ControlRecord.query.filter(ControlRecord.device == name).order_by(ControlRecord.created.desc()).first()
            )
            previous_nonoff_command = (
                ControlRecord.query.filter(ControlRecord.device == name, ControlRecord.command != "off")
                .order_by(ControlRecord.created.desc())
                .first()
            )
            data = {
                "command": latest_data.command if latest_data else None,
                "previous_command": previous_nonoff_command.command if previous_nonoff_command else None,
            }
        appliances_status: dict = dict()
        if latest_data:
            appliances_status = {
                "device_type": device_type,
                "name": name,
                "room": location,
                "time": str(latest_data.created),
                "data": data,
            }
        return appliances_status
