from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import env_config
from src.database.database.queries.triggers import NoteTriggerQuery  # to registrate

engine = create_async_engine(url=env_config.get_db_url, echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=True)
