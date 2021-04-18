from flask_restful import Resource, reqparse
from loguru import logger


from utils.oauth import GW_AUTH, g, USER_AUTH
from .model import SensorData


class SensorDataResource(Resource):
    """Save Sensor Data"""

    def __init__(self):
        # Upload Data
        self._set_post_parser()

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        data_arguments = ["temperature", "humidity"]
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
        """Upload Sensor Data"""
        logger.info(f"[Upload Sensor Data Request]\n GW: {g.gateway_name}")
        data = self.post_parser.parse_args()
        data["gateway"] = g.gateway_name
        if SensorData(**data).add():
            return {"message": "Success"}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get Latest Sensor Data"""
        logger.info(f"[GET One Sensor Data Request]\n User: {g.account}")
        data = SensorData.query.filter_by(sensor="DHT22_VLDB").order_by(SensorData.created.desc()).first()
        if data:
            return {"temperature": data.temperature, "humidity": data.humidity}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201
