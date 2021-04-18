import os

import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DB_URL", "postgresql://dev_user:dev191026@localhost:5432/dev_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# db = SQLAlchemy()
# pylint: enable=C0103

TZ = pytz.timezone(os.environ.get("TZ", "Asia/Taipei"))

REDIS_URL = os.environ.get("REDIS_URL", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_CHECK_INTERVAL = int(os.environ.get("REDIS_CHECK_INTERVAL", 600))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "password")
REDIS = redis.Redis(
    host=REDIS_URL, port=REDIS_PORT, db=0, health_check_interval=REDIS_CHECK_INTERVAL, password=REDIS_PASSWORD
)

# FOR PI
DATA_CENTER_URL = os.environ.get("DATA_CENTER_URL", "10.8.2.101:5000")
