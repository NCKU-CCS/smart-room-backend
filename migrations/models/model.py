from dataclasses import dataclass
import secrets

from sqlalchemy import Column, String, Float
from sqlalchemy.schema import UniqueConstraint

from .utilities import BASE, BaseMixin


@dataclass
class ControlRecord(BASE, BaseMixin):
    # TODO: Relationship: device -> Device.name; trigger -> user.name
    __tablename__ = "control_record"
    command: str = Column(String(), unique=False, nullable=False)
    device: str = Column(String(), unique=False, nullable=False)
    trigger: str = Column(String(), unique=False, nullable=False)


@dataclass
class Device(BASE, BaseMixin):
    __tablename__ = "device"
    name: str = Column(String(), nullable=False)
    location: str = Column(String(), nullable=False)
    room: str = Column(String(), nullable=False)
    url: str = Column(String(), unique=False, nullable=False)
    token: secrets.token_hex = Column(String(), unique=False, nullable=False)
    __table_args__ = (UniqueConstraint(name, location, room),)


@dataclass
class Gateway(BASE, BaseMixin):
    __tablename__ = "gateway"
    name: str = Column(String(), unique=True, nullable=False)
    token: secrets.token_hex = Column(String(), unique=True, nullable=False, default=secrets.token_hex())


@dataclass
class MeterData(BASE, BaseMixin):
    # TODO: Relationship: sensor -> sensor.name; gateway -> gateway.name
    __tablename__ = "meter_data"
    voltage: float = Column(Float(), comment="V")
    current: float = Column(Float(), comment="A")
    power: float = Column(Float(), comment="W")
    total_current: float = Column(Float(), comment="kWh")
    sensor: str = Column(String(), nullable=False, comment="sensor name")
    gateway: str = Column(String(), nullable=False, comment="gateway name")


@dataclass
class Sensor(BASE, BaseMixin):
    __tablename__ = "sensor"
    name: str = Column(String(), nullable=False)
    location: str = Column(String(), nullable=False)
    room: str = Column(String(), nullable=False)
    device_type: str = Column(String(), nullable=False)
    __table_args__ = (UniqueConstraint(name, location, room),)


@dataclass
class SensorData(BASE, BaseMixin):
    # TODO: Relationship: sensor -> sensor.name; gateway -> gateway.name
    __tablename__ = "sensor_data"
    temperature: float = Column(Float(), comment="celsius")
    humidity: float = Column(Float())
    sensor: str = Column(String(), nullable=False, comment="sensor name")
    gateway: str = Column(String(), nullable=False, comment="gateway name")


@dataclass
class User(BASE, BaseMixin):
    __tablename__ = "user"
    account: str = Column(String(), unique=True, nullable=False)
    password: str = Column(String(), unique=False, nullable=False)
    token: secrets.token_hex = Column(String(), unique=True, nullable=False)
