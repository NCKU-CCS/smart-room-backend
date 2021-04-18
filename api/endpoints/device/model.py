import secrets
from dataclasses import dataclass

from sqlalchemy.schema import UniqueConstraint

from config import db
from utils.base_models import BaseMixin


@dataclass
class Device(db.Model, BaseMixin):
    __tablename__ = "device"
    name: str = db.Column(db.String(), nullable=False)
    location: str = db.Column(db.String(), nullable=False)
    url: str = db.Column(db.String(), unique=False, nullable=False)
    token: secrets.token_hex = db.Column(db.String(), unique=False, nullable=False)
    __table_args__ = (UniqueConstraint(name, location),)
