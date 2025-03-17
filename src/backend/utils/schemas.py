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
    def check_title_not_empty(cls, v):
        if not v or v.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.TITLE_EMPTY.value)
        word_count = len(v.split())
        if word_count > 100:
            raise InputLengthFieldError(ErrorMessages.TITLE_TOO_LONG.value)
        return v

    @field_validator("content")
    def check_content_word_count(cls, v):
        if not v or v.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.CONTENT_EMPTY.value)
        word_count = len(v.split())
        if word_count > 500:
            raise InputLengthFieldError(ErrorMessages.CONTENT_TOO_LONG.value)
        return v


class NotePutSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    class Config:
        extra = "forbid"

    @field_validator("title")
    def check_title_not_empty(cls, v):
        if v and len(v.split()) > 100:
            raise InputLengthFieldError(ErrorMessages.TITLE_TOO_LONG.value)

        if v is not None and v.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.TITLE_EMPTY.value)
        return v

    @field_validator("content")
    def check_content_not_empty(cls, v):
        if v and len(v.split()) > 500:
            raise InputLengthFieldError(ErrorMessages.CONTENT_TOO_LONG.value)

        if v is not None and v.strip() == "":
            raise InputEmptyFieldError(ErrorMessages.CONTENT_EMPTY.value)
        return v

    @model_validator(mode="before")
    def check_title_and_content(cls, values):
        title, content = values.get("title"), values.get("content")

        if title is None and content is None:
            raise InputEmptyFieldError(ErrorMessages.FIELDS_BOTH_EMPTY.value)

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