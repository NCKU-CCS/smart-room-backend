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
        sensors = Sensor.query.filter(*criteria_sensor).all()
        appliances_status = []
        for sensor in sensors:
            latest_data = (
                SensorData.query.filter(SensorData.sensor == sensor.name).order_by(SensorData.created.desc()).first()
            )
            if latest_data:
                appliances_status.append(
                    {
                        "device_type": "thermo_sensor",
                        "name": sensor.name,
                        "room": sensor.room,
                        "time": str(latest_data.created),
                        "data": {"temperature": latest_data.temperature, "humidity": latest_data.humidity},
                    }
                )
        devices = Device.query.filter(*criteria_device).all()
        for device in devices:
            latest_data = (
                ControlRecord.query.filter(ControlRecord.device == device.name)
                .order_by(ControlRecord.created.desc())
                .first()
            )
            if latest_data:
                appliances_status.append(
                    {
                        "device_type": "ac",
                        "name": device.name,
                        "room": device.room,
                        "time": str(latest_data.created),
                        "data": {"command": latest_data.command},
                    }
                )
                if latest_data.command == "off":
                    previous_command = (
                        ControlRecord.query.filter(ControlRecord.device == device.name, ControlRecord.command != "off")
                        .order_by(ControlRecord.created.desc())
                        .first()
                    )
                    if previous_command:
                        appliances_status[-1]["data"]["previous_command"] = previous_command.command
        return appliances_status

    # pylint: enable=R0201
