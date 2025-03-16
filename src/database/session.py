from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import env_config
from src.database.database.triggers import NoteTriggerQuery

engine = create_async_engine(url=env_config.get_db_url, echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# only 1 dependency
SessionDepends = Annotated[AsyncSession, Depends(get_session)]

_ = NoteTriggerQuery  # to registrate
