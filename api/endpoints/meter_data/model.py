from dataclasses import dataclass

from config import db
from utils.base_models import BaseMixin


@dataclass
class MeterData(db.Model, BaseMixin):
    # TODO: Relationship: sensor -> sensor.name; gateway -> gateway.name
    __tablename__ = "meter_data"
    voltage: float = db.Column(db.Float(), comment="V")
    current: float = db.Column(db.Float(), comment="A")
    power: float = db.Column(db.Float(), comment="W")
    total_current: float = db.Column(db.Float(), comment="kWh")
    sensor: str = db.Column(db.String(), nullable=False, comment="sensor name")
    gateway: str = db.Column(db.String(), nullable=False, comment="gateway name")
