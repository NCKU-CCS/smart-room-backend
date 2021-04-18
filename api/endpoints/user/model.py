from dataclasses import dataclass
import secrets

from config import db
from utils.base_models import BaseMixin

@dataclass
class User(db.Model, BaseMixin):
    __tablename__ = "user"
    account: str = db.Column(db.String(), unique=True, nullable=False)
    password: str = db.Column(db.String(), unique=False, nullable=False)
    token: secrets.token_hex = db.Column(db.String(), unique=True, nullable=False)
