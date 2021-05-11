from dataclasses import dataclass
from sqlalchemy import Column, String
from config import BASE
from utils.base_models import BaseMixin


@dataclass
class ControlRecord(BASE, BaseMixin):
    # TODO: Relationship: device -> Device.name; trigger -> user.name
    __tablename__ = "control_record"
    command: str = Column(String(), unique=False, nullable=False)
    device: str = Column(String(), unique=False, nullable=False)
    trigger: str = Column(String(), unique=False, nullable=False)
