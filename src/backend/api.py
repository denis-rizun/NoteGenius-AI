from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.exceptions import RequestValidationError

from src.backend.utils.enums import ErrorMessages
from src.backend.utils.exceptions import InputLengthFieldError, InputEmptyFieldError
from src.backend.utils.helper import ApiHelper
from src.backend.utils.schemas import NotePostSchema, NotePutSchema
from src.database.session import SessionDepends


crud_router = APIRouter(
    tags=["crud"],
    prefix="/crud"
)


@crud_router.post(
    path="/post",
    summary="Create a new note",
    description="<h1>Creates a new note in the database with the provided data.</h1>"
)
async def create_note(data: NotePostSchema, session: SessionDepends):
    data_dict = dict(data)
    data_dict["version_number"] = 1
    return await ApiHelper.create_note(data=data_dict, session=session)


@crud_router.get(
    path="/get/{id}",
    summary="Get note by ID",
    description="<h1>Fetches a note from the database based on the provided ID.</h1>"
)
async def get_note_by_id(id: int, session: SessionDepends):
    return await ApiHelper.get_note_by_id(id=id, session=session)


@crud_router.get(
    path="/get",
    summary="Get all notes",
    description="<h1>Fetches all notes stored in the database.</h1>"
)
async def get_all_notes(session: SessionDepends):
    return await ApiHelper.get_all_notes(session=session)


@crud_router.put(
    path="/update/{id}",
    summary="Update a note",
    description="<h1>Updates an existing note in the database based on the provided ID and data.</h1>"
)
async def update_note(id: int, data: NotePutSchema, session: SessionDepends):
    updated_data = data.model_dump(exclude_unset=True)
    return await ApiHelper.update_note(id=id, session=session, data=updated_data)


@crud_router.delete(
    path="/delete/{id}",
    summary="Delete a note",
    description="<h1>Deletes a note from the database based on the provided ID.</h1>"
)
async def delete_note(id: int, session: SessionDepends):
    return await ApiHelper.delete_note(id=id, session=session)


analytics_router = APIRouter(
    tags=["analytics"],
    prefix="/analytics"
)


@analytics_router.get(
    path="/total_words",
    summary="Get total words",
    description="<h1>Get total words from all notes in database</h1>"
)
async def total_words(session: SessionDepends):
    return await ApiHelper.get_total_word_count(session=session)


@analytics_router.get(
    path="/length",
    summary="Get average length",
    description="<h1>Get average note length from all notes in database</h1>"
)
async def length(session: SessionDepends):
    return await ApiHelper.get_average_note_length(session=session)


@analytics_router.get(
    path="/common_words",
    summary="Get most common words",
    description="<h1>Get most common words from all notes in database</h1>"
)
async def common_words(session: SessionDepends, min_count: int = 3):
    return await ApiHelper.get_most_common_words(session=session, min_count=min_count)


@analytics_router.get(
    path="/longest",
    summary="Get the longest notes",
    description="<h1>Get the longest notes from all notes in database</h1>"
)
async def longest(session: SessionDepends, top_n: int = 3):
    return await ApiHelper.get_longest_notes(session=session, top_n=top_n)


@analytics_router.get(
    path="/shortest",
    summary="Get the shortest notes",
    description="<h1>Get the shortest notes from all notes in database</h1>"
)
async def shortest(session: SessionDepends, top_n: int = 3):
    return await ApiHelper.get_shortest_notes(session=session, top_n=top_n)


app = FastAPI(
    title="AI-powered Notes Management",
    description="Welcome to NoteGenius's API documentation! "
                "Here you will able to discover all of the ways you can interact with the NoteGenius API.",
    root_path="/api/v1",
)


app.include_router(crud_router)
app.include_router(analytics_router)


@app.exception_handler(InputEmptyFieldError)
async def validation_exception_handler(request: Request, exc: InputEmptyFieldError):
    raise HTTPException(status_code=400, detail=str(exc))


@app.exception_handler(InputLengthFieldError)
async def input_data_length_exception_handler(request: Request, exc: InputLengthFieldError):
    raise HTTPException(status_code=400, detail=str(exc))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(status_code=400, detail=ErrorMessages.NOT_CONFORM_SCHEMA.value)




