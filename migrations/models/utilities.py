"""Database related functions, like Mixins and custom data types"""
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
from sqlalchemy import Column
import sqlalchemy.types as types
from loguru import logger

from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

# pylint: disable=W0223, W0613, R0201
class UTCDatetime(types.TypeDecorator):
    impl = types.TIMESTAMP

    def process_bind_param(self, value, dialect):
        """change timezone before insert to db"""
        return value.astimezone(timezone.utc).replace(tzinfo=None) if value else None


class UUID2STR(types.TypeDecorator):
    impl = UUID(as_uuid=True)

    def process_result_value(self, value, dialect):
        return str(value)


# pylint: enable=W0223, W0613, R0201


def db_handler(func):
    def applicator(*args, **kwargs):
        try:
            session: Session = args[1]
            func(*args, **kwargs)
            return True
        except Exception as err:
            logger.error(f"DB Operation Failed.\nError: {err}")
            session.rollback()
    return applicator


@dataclass
class BaseMixin:
    uuid: UUID = Column(
        UUID2STR, primary_key=True, unique=True, nullable=False, server_default=sa_text("uuid_generate_v4()")
    )
    created: datetime = Column(UTCDatetime, default=datetime.now)

    @db_handler
    def add(self, session: Session):
        session.add(self)
        session.commit()

    # pylint: disable=R0201
    @db_handler
    def update(self, session: Session):
        session.commit()

    # pylint: enable=R0201

    @db_handler
    def delete(self, session: Session):
        session.delete(self)
        session.commit()
