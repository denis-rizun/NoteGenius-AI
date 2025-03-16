from functools import wraps

from fastapi import HTTPException
from pydantic import ValidationError

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
        except DatabaseError:
            raise HTTPException(
                status_code=500,
                detail="Oops... We ran into an unexpected problem. Please try again later.",
            )
        except DuplicateDataError:
            raise HTTPException(
                status_code=400,
                detail="The provided data violates unique constraints. Please ensure the data is unique and try again.",
            )
        except ValidationError:
            raise HTTPException(
                status_code=400,
                detail="The provided data is invalid. Please carefully review the expected data schema and try again.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"check {str(e)}",
            )

    return wrapper
