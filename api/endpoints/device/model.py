import secrets
from dataclasses import dataclass
from sqlalchemy import Column, String
from sqlalchemy.schema import UniqueConstraint
from config import BASE

from utils.base_models import BaseMixin


@dataclass
class Device(BASE, BaseMixin):
    __tablename__ = "device"
    name: str = Column(String(), nullable=False)
    location: str = Column(String(), nullable=False)
    room: str = Column(String(), nullable=False)
    url: str = Column(String(), unique=False, nullable=False)
    token: secrets.token_hex = Column(String(), unique=False, nullable=False)
    __table_args__ = (UniqueConstraint(name, location, room),)
