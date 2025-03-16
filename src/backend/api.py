from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.backend.utils.helper import ApiHelper
from src.backend.utils.schemas import (
    NotePostSchema,
    NotePutSchema,
)
from src.database.database.models import Base, NoteModel, NoteVersionModel
from src.database.session import engine, SessionDepends


app = FastAPI(
    title="AI-powered Notes Management",
    description="Welcome to NoteGenius's API documentation! Here you will able to discover all of the ways you can interact with the NoteGenius API.",
    root_path="/api/v1",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(
        status_code=400,
        detail="The input data is invalid. Please verify the provided information for accuracy.",
    )


# ----------------------temp----------------------
@app.get("/configure")
async def configure_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[NoteModel.__table__, NoteVersionModel.__table__],
        )
    return 200


# ----------------------temp----------------------


@app.post(
    path="/post",
    summary="Create a new note",
    description="<h1>Creates a new note in the database with the provided data.</h1>",
)
async def create_note(data: NotePostSchema, session: SessionDepends):
    data_dict = data.model_dump()
    data_dict["version_number"] = 1
    return await ApiHelper.create(data=data, session=session)



@app.get(
    path="/get/{id}",
    summary="Get note by ID",
    description="<h1>Fetches a note from the database based on the provided ID.</h1>",
)
async def get_by_id_note(id: int, session: SessionDepends):
    return await ApiHelper.get_by_id(id, session)


@app.get(
    path="/get",
    summary="Get all notes",
    description="<h1>Fetches all notes stored in the database.</h1>",
)
async def get_all_notes(session: SessionDepends):
    return await ApiHelper.get_all(session)


@app.put(
    path="/put/{id}",
    summary="Update a note",
    description="<h1>Updates an existing note in the database based on the provided ID and data.</h1>",
)
async def put_note(id: int, data: NotePutSchema, session: SessionDepends):
    obj = await ApiHelper.get_by_id(id, session)
    return await ApiHelper.put(obj, session, data)


@app.delete(
    path="/delete/{id}",
    summary="Delete a note",
    description="<h1>Deletes a note from the database based on the provided ID.</h1>",
)
async def delete_note(id: int, session: SessionDepends):
    obj = await ApiHelper.get_by_id(id, session)
    return await ApiHelper.delete(obj, session)
