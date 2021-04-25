import secrets
from dataclasses import dataclass
from sqlalchemy import Column, String
from config import BASE
from utils.base_models import BaseMixin


@dataclass
class Gateway(BASE, BaseMixin):
    __tablename__ = "gateway"
    name: str = Column(String(), unique=True, nullable=False)
    token: secrets.token_hex = Column(String(), unique=True, nullable=False, default=secrets.token_hex())
