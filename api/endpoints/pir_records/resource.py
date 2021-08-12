from flask_restful import Resource, reqparse
from loguru import logger

from config import SESSION
from utils.oauth import GW_AUTH, g
from database.migrations.models import PirRecords


class PirRecordsResource(Resource):
    """Save Pir Records (motion sensor)"""

    def __init__(self):
        # Upload Data
        self._set_post_parser()

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            "device_id", type=str, required=True, location="json", help="Upload Pir: device_id is required"
        )
        self.post_parser.add_argument(
            "created", type=str, required=True, location="json", help="Upload Pir: device_id is required"
        )
        self.post_parser.add_argument(
            "status", type=int, required=True, location="json", help="Upload Pir: status is required"
        )

    # pylint: disable=R0201
    @GW_AUTH.login_required
    def post(self):
        """Upload Pir Records"""
        logger.info(f"[Upload Pir Records Request]\n GW: {g.gateway_name}")
        data = self.post_parser.parse_args()
        if PirRecords(**data).add(SESSION):
            return {"message": "Success"}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201
