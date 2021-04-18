from dataclasses import dataclass

from config import db
from utils.base_models import BaseMixin


@dataclass
class SensorData(db.Model, BaseMixin):
    # TODO: Relationship: sensor -> sensor.name; gateway -> gateway.name
    __tablename__ = "sensor_data"
    temperature: float = db.Column(db.Float(), comment="celsius")
    humidity: float = db.Column(db.Float())
    sensor: str = db.Column(db.String(), nullable=False, comment="sensor name")
    gateway: str = db.Column(db.String(), nullable=False, comment="gateway name")
