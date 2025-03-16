from functools import wraps

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.backend.utils.exceptions import DatabaseError, DuplicateDataError


def handle_sqlalchemy_error(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IntegrityError as e:  # log it
            raise DuplicateDataError(str(e))
        except SQLAlchemyError as e:  # log it
            raise DatabaseError(str(e))

    return wrapper
