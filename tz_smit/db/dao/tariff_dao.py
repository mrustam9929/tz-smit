from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tz_smit.db.dao.base import BaseDAO
from tz_smit.db.dependencies import get_db_session
from tz_smit.db.models.tariff import TariffModel


class TariffDAO(BaseDAO):
    """Class for accessing dummy table."""

    model = TariffModel


def get_tariff_dao(session: AsyncSession = Depends(get_db_session)) -> TariffDAO:
    return TariffDAO(session=session)
