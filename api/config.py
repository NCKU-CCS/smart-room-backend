import os

import pytz
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import redis


load_dotenv()


class Config:
    """Parent configuration class."""

    DEBUG = False
    CSRF_ENABLED = True
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL", "postgresql://dev_user:devpw@localhost:5432/dev_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


APP_CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}


# pylint: disable=C0103
app = Flask(__name__)
# pylint: enable=C0103
ENGINE: Engine = create_engine(
    os.environ.get("DB_URL", "postgresql://postgres:password@localhost:5432/database"), pool_pre_ping=True
)
SESSION: Session = sessionmaker(bind=ENGINE)()
BASE = declarative_base()

TZ = pytz.timezone(os.environ.get("TZ", "Asia/Taipei"))
TZ_OFFSET = int(os.environ.get("TZ_OFFSET", 8))

REDIS_CHECK_INTERVAL = int(os.environ.get("REDIS_CHECK_INTERVAL", 600))
REDIS = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://:password@localhost:6379/0"), health_check_interval=REDIS_CHECK_INTERVAL
)

# AIR_CONDITIONER_VOLTAGE
VOLTAGE = int(os.environ.get("AIR_CONDITIONER_VOLTAGE", 220))

# AIR_CONDITIONER_VOLTAGE
NORMAL_VOLTAGE = int(os.environ.get("NORMAL_VOLTAGE", 110))

# Outdoor thermo sensor
OUTDOOR_THERMO_SENSORS = os.environ.get("OUTDOOR_THERMO_SENSORS", "DHT11_OUTDOOR").split(",")
