from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    version_number: Mapped[int]


class NoteModel(Base):
    __tablename__ = "note"

    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    # one Note can have many NoteVersions
    versions: Mapped[list["NoteVersionModel"]] = relationship(
        argument="NoteVersionModel",
        back_populates="note",
        cascade="all, delete",
    )


class NoteVersionModel(Base):
    __tablename__ = "note_version"

    title: Mapped[str]
    note_id: Mapped[int] = mapped_column(ForeignKey("note.id"))

    # many NoteVersions belong to one Note
    note: Mapped["NoteModel"] = relationship(
        argument="NoteModel",
        back_populates="versions",
    )
