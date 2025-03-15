import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database.models import NoteModel

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


class NoteQuery:
    MODEL = NoteModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> None:
        try:
            obj = NoteModel(**data)
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)

            await self.session.commit()
        except SQLAlchemyError as e:
            print(e)  # own exception

    async def get_by_id(self, id: int) -> NoteModel:
        try:
            stmt = select(NoteModel).where(self.MODEL.id == id)
            res = await self.session.execute(stmt)
            obj = res.scalar_one_or_none()
            if not obj:
                ...  # own exception, 204 not content

            return obj
        except SQLAlchemyError as e:
            print(e)  # own exception

    async def get_all(self) -> list[NoteModel]:
        try:
            stmt = select(self.MODEL)
            res = await self.session.execute(stmt)
            data = res.scalars().all()
            if not data:
                ...  # own exception, 204 not content

            return data
        except SQLAlchemyError as e:
            print(e)  # own exception

    async def put(self, obj: NoteModel, data: dict) -> None:
        try:
            await asyncio.sleep(2)
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            obj.version_number += 1
            await self.session.commit()
        except SQLAlchemyError as e:
            print(e)  # own exception

    async def delete(self, obj: NoteModel) -> None:
        try:
            await self.session.delete(obj)
            await self.session.commit()
        except SQLAlchemyError as e:
            print(e)  # own exception
