from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.engine.base import Connection
from src.database.database.models import NoteModel, NoteVersionModel


class NoteTriggerQuery:
    @staticmethod
    @event.listens_for(NoteModel, "after_insert")
    @event.listens_for(NoteModel, "after_update")
    def create_version_after_insert_or_update(mapper: Mapper, connection: Connection, target: NoteModel) -> None:
        with Session(bind=connection) as sync_session:
            try:
                sync_session.add(
                    NoteVersionModel(
                        note_id=target.id,
                        title=target.title,
                        content=target.content,
                        summarization=target.summarization,
                        created_at=target.created_at,
                        version_number=target.version_number,
                    )
                )
                sync_session.commit()
            except SQLAlchemyError as e:
                sync_session.rollback()
                raise e
