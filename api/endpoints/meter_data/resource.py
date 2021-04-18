from flask_restful import Resource, reqparse
from loguru import logger


from utils.oauth import GW_AUTH, g
from .model import MeterData


class MeterDataResource(Resource):
    """Save Meter Data"""

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
