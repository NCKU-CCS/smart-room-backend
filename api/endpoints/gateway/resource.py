import secrets

from flask_restful import Resource, reqparse
from loguru import logger

from utils.start_up import update_gateways
from utils.oauth import USER_AUTH, g

from config import SESSION
from migrations.models import Gateway


class GatewayResource(Resource):
    """Gateway Management"""

    # TODO: GET, PUT Gateway

    def __init__(self):
        # Add Gateway
        self._set_post_parser()

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            "name", type=str, required=True, location="json", help="Add Gateway: name is required"
        )
        self.post_parser.add_argument("token", type=str, required=False, location="json")

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def post(self):
        """Add Gateway"""
        args = self.post_parser.parse_args()
        logger.info(f"[ADD Gateway] User: {g.account}, GW: {args['name']}")
        token = args["token"] if args["token"] else secrets.token_hex()
        if Gateway(**{"name": args["name"], "token": token}).add(SESSION):
            # Update Cache
            update_gateways()
            return {"message": "success", "token": token}
        return {"message": "Failed"}, 400

    # pylint: enable=R0201
