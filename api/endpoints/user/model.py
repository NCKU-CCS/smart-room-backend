from dataclasses import dataclass
import secrets

from sqlalchemy import Column, String
from config import BASE
from utils.base_models import BaseMixin


@dataclass
class User(BASE, BaseMixin):
    __tablename__ = "user"
    account: str = Column(String(), unique=True, nullable=False)
    password: str = Column(String(), unique=False, nullable=False)
    token: secrets.token_hex = Column(String(), unique=True, nullable=False)
