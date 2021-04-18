import json

from loguru import logger
from flask import g
from flask_httpauth import HTTPTokenAuth

from endpoints.user.model import User
from config import REDIS


GW_AUTH = HTTPTokenAuth(scheme="Bearer")
USER_AUTH = HTTPTokenAuth(scheme="Bearer")


class GatewayAuth:
    @staticmethod
    @GW_AUTH.verify_token
    def verify_token(token):
        gateway_dict = json.loads(REDIS.get("gateways"))
        if token not in gateway_dict:
            logger.error(f"[GW OAUTH Failed] token: {token}")
            g.error_message = "Access Denied"
            return False
        g.gateway_name = gateway_dict[token]
        logger.info(f"[GW OAUTH Success] GW: {g.gateway_name}")
        return True

    @staticmethod
    @GW_AUTH.error_handler
    def unauthorized():
        return {"error": g.error_message}, 401


class UserAuth:
    @staticmethod
    @USER_AUTH.verify_token
    def verify_token(token):
        user = User.query.filter_by(token=token).first()
        if user:
            logger.info(f"[User OAUTH Success] User: {user.account}")
            g.uuid = user.uuid
            g.account = user.account
            return True
        logger.error(f"[USER OAUTH Failed] token: {token}")
        g.error_message = "Access Denied"
        return False

    @staticmethod
    @USER_AUTH.error_handler
    def unauthorized():
        return {"error": g.error_message}, 401
