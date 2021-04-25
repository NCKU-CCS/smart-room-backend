import secrets

from flask_restful import Resource, reqparse
from loguru import logger

from utils.oauth import USER_AUTH, g
from .model import Device


class DeviceResource(Resource):
    """Device Management"""

    # TODO: GET, PUT Device

    def __init__(self):
        # Add Device
        self._set_post_parser()

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        device_arguments = ["name", "url", "location", "room"]
        for arg in device_arguments:
            self.post_parser.add_argument(
                arg, type=str, required=True, location="json", help=f"Create Device: {arg} is required"
            )
        self.post_parser.add_argument("token", type=str, required=False, location="json")

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def post(self):
        """Add Device"""
        args = self.post_parser.parse_args()
        logger.info(f"[ADD Device] User: {g.account}, Device: {args['name']}")
        device = {
            "name": args["name"],
            "url": args["url"],
            "room": args["room"],
            "location": args["location"],
            "token": args["token"] if args["token"] else secrets.token_hex(),
        }
        if Device(**device).add():
            return {"message": "Success"}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201
