from functools import wraps

from fastapi import HTTPException

from src.backend.utils.enums import ErrorMessages


class NoteGeniusError(Exception):
    """
    Base class for all custom exceptions in the Note Genius application.
    It extends the built-in Exception class to allow for custom error handling.
    """
    def __init__(self, message: str):
        """
        Initializes the custom exception with a message.

        Args:
            message (str): The error message that describes the exception.
        """
        super().__init__(message)


class DatabaseError(NoteGeniusError):
    """
    Exception raised for errors related to database operations.
    This can be used for database connection issues or query errors.
    """
    pass


class NotFoundError(DatabaseError):
    """
    Exception raised when a resource is not found, typically used for 404 errors.
    This indicates that the requested resource could not be found in the database.
    """
    pass


class DuplicateDataError(DatabaseError):
    """
    Exception raised when there is an attempt to insert duplicate data into the database.
    This can be used when a unique constraint violation occurs, such as inserting a duplicate record.
    """
    pass


class InputFieldError(NoteGeniusError):
    """
    Base class for exceptions related to invalid input fields.
    This can be used to signal that the provided input data is incorrect or incomplete.
    """
    pass


class InputLengthFieldError(InputFieldError):
    """
    Exception raised when the length of a field exceeds the allowed limit.
    This can be used for fields like title or content where length restrictions are enforced.
    """
    pass


class InputEmptyFieldError(InputFieldError):
    """
    Exception raised when a required field is empty or missing.
    This indicates that the user did not provide a value for a required field.
    """
    pass


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e),
            )
        except DuplicateDataError:
            raise HTTPException(
                status_code=400,
                detail=ErrorMessages.DUPLICATE_DATA.value,
            )
        except DatabaseError:
            raise HTTPException(
                status_code=500,
                detail=ErrorMessages.DATABASE_CRASHED.value,
            )

    return wrapper
