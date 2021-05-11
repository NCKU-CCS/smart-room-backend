from flask_restful import Resource, reqparse
from loguru import logger

from config import SESSION
from utils.oauth import USER_AUTH, g
from migrations.models.model import Sensor, SensorData, Device, ControlRecord


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
        sensors = SESSION.query(Sensor).filter(*criteria_sensor).all()
        for sensor in sensors:
            appliances_status.append(self.get_latest_sensor_data(sensor.device_type, sensor.name, sensor.room))
        devices = SESSION.query(Device).filter(*criteria_device).all()
        for device in devices:
            appliances_status.append(self.get_latest_sensor_data("ac", device.name, device.room))
        return appliances_status

    # pylint: enable=R0201

    @staticmethod
    def get_latest_sensor_data(device_type: str, name: str, location: str) -> dict:
        if device_type == "thermo_sensor":
            latest_command: SensorData = (
                SESSION.query(SensorData).filter(SensorData.sensor == name).order_by(SensorData.created.desc()).first()
            )
            if latest_command:
                data = {"temperature": latest_command.temperature, "humidity": latest_command.humidity}
            else:
                data = {"temperature": None, "humidity": None}
        elif device_type == "ac":
            latest_command: ControlRecord = (
                SESSION.query(ControlRecord)
                .filter(ControlRecord.device == name)
                .order_by(ControlRecord.created.desc())
                .first()
            )
            latest_control_command = (
                SESSION.query(ControlRecord)
                .filter(ControlRecord.device == name, ControlRecord.command.notin_(["off", "fan"]))
                .order_by(ControlRecord.created.desc())
                .first()
            )
            latest_mode: str = mode_judgment(latest_command)
            data = {
                "status": "ON" if latest_mode != "off" else "OFF",
                "mode": latest_mode,
                "temp": latest_control_command.command if latest_control_command else None,
            }
        appliances_status: dict = dict()
        if latest_command:
            appliances_status = {
                "device_type": device_type,
                "name": name,
                "room": location,
                "time": str(latest_command.created),
                "data": data,
            }
        return appliances_status


def mode_judgment(latest_command):
    mode: str = "off"
    if latest_command:
        if latest_command.command == "off":
            mode = "off"
        elif latest_command.command == "fan":
            mode = "fan"
        else:
            mode = "cool"
    return mode
