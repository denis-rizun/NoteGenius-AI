from functools import wraps

from fastapi import HTTPException

from src.backend.utils.enums import ErrorMessages
from src.backend.utils.exceptions import (
    DatabaseError,
    NotFoundError,
    DuplicateDataError,
)


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
