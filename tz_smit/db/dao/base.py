from operator import and_
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta

# Тип модели для DAO
ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class BaseDAO(Generic[ModelType]):
    """
    Базовый DAO-класс для работы с моделями.
    """

    model: Type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, obj_id: int) -> Optional[ModelType]:
        """
        Получить объект по ID.
        """
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """
        Получить все записи с пагинацией.
        """
        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, **obj_data) -> ModelType:
        """
        Создать новую запись.
        """
        new_obj = self.model(**obj_data)
        self.session.add(new_obj)
        await self.session.commit()
        await self.session.refresh(new_obj)
        return new_obj

    async def bulk_create(self, objects: List[Dict[str, Any]]) -> None:
        """
        Массовое создание записей.
        """
        new_objects = [self.model(**obj) for obj in objects]
        self.session.add_all(new_objects)
        await self.session.commit()

    async def update(self, obj_id: int, **update_data) -> Optional[ModelType]:
        """
        Обновить объект по ID.
        """
        query = update(self.model).where(self.model.id == obj_id).values(**update_data)
        query = query.execution_options(synchronize_session="fetch")
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_by_id(obj_id)

    async def delete(self, obj_id: int) -> bool:
        """
        Удалить объект по ID.
        """
        query = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(query)
        await self.session.commit()
        return True

    async def filter_by_fields(
        self,
        fields: Dict[str, Any],
        limit: int = 100,
        offset: int = 0,
    ) -> List[ModelType]:
        """
        Фильтрация записей по полям.
        """
        conditions = [
            getattr(self.model, key) == value for key, value in fields.items()
        ]
        query = select(self.model).where(and_(*conditions)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().all())
