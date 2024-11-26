from sqlalchemy.orm import DeclarativeBase

from tz_smit.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
