from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
import sqlalchemy.types as types
from loguru import logger

from config import db, TZ


# pylint: disable=W0223, W0613, R0201
class UTCDatetime(types.TypeDecorator):
    impl = types.TIMESTAMP

    def process_bind_param(self, value, dialect):
        """change timezone before insert to db"""
        return value.astimezone(timezone.utc).replace(tzinfo=None) if value else None

    def process_result_value(self, value, dialect):
        """change timezone after select from db"""
        return value.replace(tzinfo=timezone.utc).astimezone(TZ).replace(tzinfo=None) if value else None


class UUID2STR(types.TypeDecorator):
    impl = UUID(as_uuid=True)

    def process_result_value(self, value, dialect):
        return str(value)


# pylint: enable=W0223, W0613, R0201


def db_handler(func):
    def applicator(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except Exception as err:
            logger.error(f"DB Operation Failed.\nError: {err}")
            db.session.rollback()

    return applicator


@dataclass
class BaseMixin:
    uuid: UUID = db.Column(
        UUID2STR, primary_key=True, unique=True, nullable=False, server_default=sa_text("uuid_generate_v4()")
    )
    created: datetime = db.Column(UTCDatetime, default=datetime.now)

    @db_handler
    def add(self):
        db.session.add(self)
        db.session.commit()

    # pylint: disable=R0201
    @db_handler
    def update(self):
        db.session.commit()

    # pylint: enable=R0201

    @db_handler
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()
