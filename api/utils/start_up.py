import sys
import json

from loguru import logger

from config import SESSION, REDIS

# Have to do that to let service know migration route
# Note that it applied to all routes, so only need to do this once
# pylint: disable=C0413
sys.path.append('../')
from database.migrations.models import Gateway  # noqa: E402

# pylint: enable=C0413


def init_redis():
    """Initialize Redis Data"""
    try:
        update_gateways()
    except Exception as err:
        logger.warning(f"[INIT REDIS]: {err}")


def update_gateways():
    """Add (Refresh) Gateways to Redis"""
    # Add gateways
    gateways = SESSION.query(Gateway).all()
    gateway_dict = {gw.token: gw.name for gw in gateways}
    REDIS.set("gateways", json.dumps(gateway_dict))
    logger.info(f"[INIT REDIS] add {len(gateway_dict)} gateways")
