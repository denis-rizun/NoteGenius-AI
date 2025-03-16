class NoteGeniusError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(NoteGeniusError): ...


class DatabaseError(NoteGeniusError): ...


class DuplicateDataError(NoteGeniusError): ...


class InputDataError(NoteGeniusError): ...
