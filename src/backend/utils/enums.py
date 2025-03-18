from enum import StrEnum


class ErrorMessages(StrEnum):
    TITLE_EMPTY = "Field 'title' cannot be empty. Please provide a valid value for this field."
    CONTENT_EMPTY = "Field 'content' cannot be empty. Please provide a valid value for this field."
    TITLE_TOO_LONG = "Field 'title' exceeds the allowed word limit (100)."
    CONTENT_TOO_LONG = "Field 'content' exceeds the allowed word limit (500)."
    FIELDS_BOTH_EMPTY = "Fields 'title' & 'content' cannot be empty."
    NOT_CONFORM_SCHEMA = "Invalid data format. The provided input does not conform to the expected schema. Please ensure all fields are correctly structured and follow the specified format.",


    DUPLICATE_DATA = "The provided data violates unique constraints. Please ensure the data is unique and try again."
    DATABASE_CRASHED = "Oops... We ran into an unexpected problem. Please try again later."
    NOT_FOUND_SINGLE = "Note not found. The provided ID may be incorrect, or no data is available."
    NOT_FOUND_MULTI = "Notes not found. There may be no data available. Please try adding some notes first before interacting."