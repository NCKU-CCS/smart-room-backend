from flask import jsonify
from flask_restful import Resource, reqparse
from loguru import logger

from config import SESSION
from utils.oauth import USER_AUTH, g
from migrations.models import Sensor


class SensorResource(Resource):
    """Sensor Management"""

    def __init__(self):
        # Get Sensors
        self._set_get_parser()
        # Add Sensor
        self._set_post_parser()

    def _set_get_parser(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("name", type=str, required=False, location="values")
        self.get_parser.add_argument("room", type=str, required=False, location="values")
        self.get_parser.add_argument("location", type=str, required=False, location="values")
        self.get_parser.add_argument("device_type", type=str, required=False, location="values")

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            "name", type=str, required=True, location="json", help="Add Sensor: name is required"
        )
        self.post_parser.add_argument(
            "room", type=str, required=True, location="json", help="Add Sensor: name is required"
        )
        self.post_parser.add_argument(
            "location", type=str, required=True, location="json", help="Add Sensor: location is required"
        )
        self.post_parser.add_argument(
            "device_type", type=str, required=True, location="json", help="Add Sensor: device_type is required"
        )

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get Sensors"""
        args = self.get_parser.parse_args()
        logger.info(f"[Get Sensor] User: {g.account}")
        criteria = list()
        for argument in args:
            if args[argument]:
                criteria.append(getattr(Sensor, argument) == args[argument])
        return jsonify(SESSION.query(Sensor).filter(*criteria).all())

    # pylint: enable=R0201

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def post(self):
        """Add Sensor"""
        args = self.post_parser.parse_args()
        logger.info(f"[ADD Sensor] User: {g.account}")
        logger.debug(args)
        if Sensor(**args).add(SESSION):
            return {"message": "Success"}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201
