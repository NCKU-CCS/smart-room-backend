from flask import request
from flask_restful import Resource
from loguru import logger


class HealthResource(Resource):
    """Server Health"""

    # pylint: disable=R0201
    def get(self):
        logger.info(f"[Health] Trigger by: {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")
        return {"message": "Success"}

    # pylint: enable=R0201
