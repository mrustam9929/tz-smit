from sqlalchemy import Column, func
from sqlalchemy.sql.sqltypes import DECIMAL, BigInteger, Date, DateTime, String

from tz_smit.db.base import Base


class TariffModel(Base):
    __tablename__ = "tariffs"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    cargo_type = Column(String(255), nullable=False, index=True)
    rate = Column(DECIMAL(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
