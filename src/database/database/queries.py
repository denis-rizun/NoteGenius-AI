from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database.decorator import handle_sqlalchemy_error
from src.database.database.models import NoteModel


class NoteQuery:
    """Database operations for NoteModel."""

    __MODEL = NoteModel

    def __init__(self, session: AsyncSession):
        """Initialize NoteQuery with an async database session."""
        self.session = session

    @handle_sqlalchemy_error
    async def create(self, data: dict) -> NoteModel:
        """Create a new note and return its ID."""
        obj = self.__MODEL(**data)
        self.session.add(obj)
        await self.session.commit()
        return obj.id

    @handle_sqlalchemy_error
    async def get_by_id(self, id: int) -> Optional[NoteModel]:
        """Retrieve a note by its ID."""
        stmt = select(self.__MODEL).where(self.__MODEL.id == id)
        res = await self.session.execute(stmt)
        obj = res.scalar_one_or_none()
        return obj

    @handle_sqlalchemy_error
    async def get_all(self) -> Optional[list[NoteModel]]:
        """Retrieve all notes."""
        stmt = select(self.__MODEL)
        res = await self.session.execute(stmt)
        objs = res.scalars().all()
        return objs

    @handle_sqlalchemy_error
    async def put(self, obj: NoteModel, data: dict) -> None:
        """Update a note with new data."""
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        obj.version_number += 1
        await self.session.commit()

    @handle_sqlalchemy_error
    async def delete(self, obj: NoteModel) -> None:
        """Delete a note from the database."""
        await self.session.delete(obj)
        await self.session.commit()