from dataclasses import dataclass
from sqlalchemy import Column, String, Float
from config import BASE
from utils.base_models import BaseMixin


@dataclass
class MeterData(BASE, BaseMixin):
    # TODO: Relationship: sensor -> sensor.name; gateway -> gateway.name
    __tablename__ = "meter_data"
    voltage: float = Column(Float(), comment="V")
    current: float = Column(Float(), comment="A")
    power: float = Column(Float(), comment="W")
    total_current: float = Column(Float(), comment="kWh")
    sensor: str = Column(String(), nullable=False, comment="sensor name")
    gateway: str = Column(String(), nullable=False, comment="gateway name")
