from dataclasses import dataclass

from sqlalchemy.schema import UniqueConstraint

from config import db
from utils.base_models import BaseMixin


@dataclass
class Sensor(db.Model, BaseMixin):
    __tablename__ = "sensor"
    name: str = db.Column(db.String(), nullable=False)
    location: str = db.Column(db.String(), nullable=False)
    device_type: str = db.Column(db.String(), nullable=False)
    __table_args__ = (UniqueConstraint(name, location),)
