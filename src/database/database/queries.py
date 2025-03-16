from typing import Optional

from sqlalchemy import select

from src.database.database.abstraction import Query
from src.database.database.decorator import handle_sqlalchemy_error
from src.database.database.models import NoteModel


class NoteQuery(Query):
    __MODEL = NoteModel

    @handle_sqlalchemy_error
    async def create(self, data: dict) -> NoteModel:
        obj = self.__MODEL(**data)
        self.session.add(obj)
        await self.session.commit()
        return obj.id

    @handle_sqlalchemy_error
    async def get_by_id(self, id: int) -> Optional[NoteModel]:
        stmt = select(self.__MODEL).where(self.__MODEL.id == id)
        res = await self.session.execute(stmt)
        obj = res.scalar_one_or_none()
        return obj

    @handle_sqlalchemy_error
    async def get_all(self) -> Optional[list[NoteModel]]:
        stmt = select(self.__MODEL)
        res = await self.session.execute(stmt)
        objs = res.scalars().all()
        return objs

    @handle_sqlalchemy_error
    async def put(self, obj: NoteModel, data: dict) -> None:
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        obj.version_number += 1
        await self.session.commit()

    @handle_sqlalchemy_error
    async def delete(self, obj: NoteModel) -> None:
        await self.session.delete(obj)
        await self.session.commit()
