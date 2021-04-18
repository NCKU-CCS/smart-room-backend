import json

from loguru import logger

from endpoints.gateway.model import Gateway
from config import REDIS


def init_redis():
    """Initialize Redis Data"""
    update_gateways()


def update_gateways():
    """Add (Refresh) Gateways to Redis"""
    # Add gateways
    gateways = Gateway.query.all()
    gateway_dict = {gw.token: gw.name for gw in gateways}
    REDIS.set("gateways", json.dumps(gateway_dict))
    logger.info(f"[INIT REDIS] add {len(gateway_dict)} gateways")
