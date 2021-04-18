import secrets
from dataclasses import dataclass

from config import db
from utils.base_models import BaseMixin


@dataclass
class Gateway(db.Model, BaseMixin):
    __tablename__ = "gateway"
    name: str = db.Column(db.String(), unique=True, nullable=False)
    token: secrets.token_hex = db.Column(db.String(), unique=True, nullable=False, default=secrets.token_hex())
