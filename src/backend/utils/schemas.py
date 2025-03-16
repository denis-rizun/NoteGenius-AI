from typing import Optional

from pydantic import BaseModel, model_validator

from src.backend.utils.exceptions import InputDataError


class NotePostSchema(BaseModel):
    title: str
    content: str

    class Config:
        extra = "forbid"

    @model_validator(mode="before")
    def check_fields(cls, values):
        title, content = values.get("title"), values.get("content")

        if title is None or content is None:
            raise InputDataError("")
        return values


class NoteGetSchemaResponse(BaseModel):
    id: int
    title: str
    content: str
    summarization: str
    version_number: int
    created_at: str
    updated_at: str

    class ConfigDict:
        from_attributes = True


class NotePutSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    class Config:
        extra = "forbid"

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        title, content = values.get("title"), values.get("content")

        if title is None and content is None:
            raise InputDataError("")
        return values
