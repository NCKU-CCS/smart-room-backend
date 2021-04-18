from dataclasses import dataclass

from config import db
from utils.base_models import BaseMixin


@dataclass
class ControlRecord(db.Model, BaseMixin):
    # TODO: Relationship: device -> Device.name; trigger -> user.name
    __tablename__ = "control_record"
    command: str = db.Column(db.String(), unique=False, nullable=False)
    device: str = db.Column(db.String(), unique=False, nullable=False)
    trigger: str = db.Column(db.String(), unique=False, nullable=False)
