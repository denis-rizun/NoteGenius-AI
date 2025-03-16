from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database.models import Base

TBase = TypeVar("TBase", bound=Base)


class Query(ABC, Generic[TBase]):
    __MODEL: TBase = ...

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, data: dict) -> int: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[TBase]: ...

    @abstractmethod
    async def get_all(self) -> Optional[list[TBase]]: ...

    @abstractmethod
    async def put(self, obj: TBase, data: dict) -> None: ...

    @abstractmethod
    async def delete(self, obj: TBase) -> None: ...
