import socket
import json

from flask_restful import Resource, reqparse
from loguru import logger

from config import SESSION
from utils.oauth import USER_AUTH, g
from migrations.models import ControlRecord, Device


class ControlResource(Resource):
    """Device Control and Record"""

    def __init__(self):
        # Get Device Status
        self._set_get_parser()
        # Control Device
        self._set_post_parser()

    def _set_get_parser(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("device", required=True, location="values", help="device is required")

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            "device", type=str, required=True, location="json", help=f"Control: device is required"
        )
        available_commands = [str(temperature) + "C" for temperature in range(16, 31)]
        available_commands.extend(["off", "fan"])
        self.post_parser.add_argument(
            "command",
            type=str,
            choices=available_commands,
            required=True,
            location="json",
            help=f"Control: command is required, must be [16-30]C or off",
        )

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def post(self):
        """Control Device and Save Record"""
        args = self.post_parser.parse_args()
        logger.info(f"[Control Device] Device: {args['device']}, Command: {args['command']}, Trigger: {g.account}")
        device = SESSION.query(Device).filter_by(name=args["device"]).first()
        if not device:
            return {"message": "Device Not Found"}, 400
        response = control_device(device, args["command"])
        if response:
            record = {"device": args["device"], "command": args["command"], "trigger": g.account}
            if ControlRecord(**record).add(SESSION):
                return {"message": "Control Success"}
            return {"message": "Control Success, Save Failed"}, 500
        return {"message": "Control Failed"}, 400

    # pylint: enable=R0201

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get Latest Device Status"""
        logger.info(f"[GET Device Status Request]\n User: {g.account}")
        args = self.get_parser.parse_args()
        # TODO: Add location
        data = (
            SESSION.query(ControlRecord).filter_by(device=args["device"]).order_by(ControlRecord.created.desc()).first()
        )
        if data:
            return {"status": data.command}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201


def control_device(device: Device, command: str) -> bool:
    """Send Control Command

    Args:
        device (Device): Control Device
        command (str): command

    Returns:
        bool: success or failed
    """
    logger.info("[Control Device] Send Command")
    host, port = device.url.split(":")
    command = {"command": command, "token": device.token}
    receive_data = send_socket(host, int(port), json.dumps(command))
    if receive_data == "True":
        return True
    return False


def send_socket(host: str, port: int, data: str) -> str:
    """Send Socket to Slave

    Args:
        host (str): host
        port (int): port
        data (str): command

    Returns:
        str: receive string
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        sock.send(data.encode())
        receive_data = sock.recv(1024).decode()
        sock.close()
    except socket.error as msg:
        logger.error(f"[Socket Error] {msg}")
        return False
    return receive_data
