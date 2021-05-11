from dataclasses import dataclass

from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import Column, String
from config import BASE
from utils.base_models import BaseMixin


@dataclass
class Sensor(BASE, BaseMixin):
    __tablename__ = "sensor"
    name: str = Column(String(), nullable=False)
    location: str = Column(String(), nullable=False)
    room: str = Column(String(), nullable=False)
    device_type: str = Column(String(), nullable=False)
    __table_args__ = (UniqueConstraint(name, location, room),)
