from dataclasses import dataclass

from sqlalchemy import Column, String, Float
from config import BASE
from utils.base_models import BaseMixin


@dataclass
class SensorData(BASE, BaseMixin):
    # TODO: Relationship: sensor -> sensor.name; gateway -> gateway.name
    __tablename__ = "sensor_data"
    temperature: float = Column(Float(), comment="celsius")
    humidity: float = Column(Float())
    sensor: str = Column(String(), nullable=False, comment="sensor name")
    gateway: str = Column(String(), nullable=False, comment="gateway name")
