from typing import Optional

from pydantic import BaseModel, model_validator, field_validator

from src.backend.utils.enums import ErrorMessages
from src.backend.utils.exceptions import InputLengthFieldError, InputEmptyFieldError


class NotePostSchema(BaseModel):
    title: str
    content: str

    class Config:
        extra = "forbid"

    @field_validator("title")
    def check_title_not_empty(cls, value):
        if not value or value.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.TITLE_EMPTY.value)
        word_count = len(value.split())
        if word_count > 100:
            raise InputLengthFieldError(ErrorMessages.TITLE_TOO_LONG.value)
        return value

    @field_validator("content")
    def check_content_word_count(cls, value):
        if not value or value.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.CONTENT_EMPTY.value)
        word_count = len(value.split())
        if word_count > 500:
            raise InputLengthFieldError(ErrorMessages.CONTENT_TOO_LONG.value)
        return value


class NotePostSchemaResponse(BaseModel):
    note_id: int


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

    @field_validator("title")
    def check_title_not_empty(cls, value):
        if value and len(value.split()) > 100:
            raise InputLengthFieldError(ErrorMessages.TITLE_TOO_LONG.value)

        if value is not None and value.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.TITLE_EMPTY.value)
        return value

    @field_validator("content")
    def check_content_not_empty(cls, value):
        if value and len(value.split()) > 500:
            raise InputLengthFieldError(ErrorMessages.CONTENT_TOO_LONG.value)

        if value is not None and value.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.CONTENT_EMPTY.value)
        return value

    @model_validator(mode="before")
    def check_title_and_content(cls, values):
        title, content = values.get("title"), values.get("content")

        if title is None and content is None:
            raise InputEmptyFieldError(ErrorMessages.FIELDS_BOTH_EMPTY.value)

        return values


class WordCountSchemaResponse(BaseModel):
    word_count: int


class AVGNoteLengthSchemaResponse(BaseModel):
    average_note_length: float