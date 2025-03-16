from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError

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
    data_dict = dict(data)
    data_dict["version_number"] = 1
    return await ApiHelper.create_note(data=data_dict, session=session)


# {
#   "title": "Project Update: March 2025",
#   "content": "Today, we made significant progress on the AI-powered resume screening project. We successfully integrated the new recommendation engine, which will enhance the accuracy of candidate suggestions. The team also completed a major update to the database, improving query speed and reliability. A few issues remain with data inconsistency, but the engineering team is already working on a solution. We expect to have this fixed by the end of the week. Next steps involve finalizing the API documentation and preparing for the internal demo scheduled for next month."
# }
# {
#   "title": "Quarterly Financial Report Q1 2025",
#   "content": "The financial performance for the first quarter of 2025 has shown promising results. Revenue for the quarter increased by 15% compared to Q1 2024, driven by a strong demand for our flagship products. Gross profit margin remained steady at 38%, despite higher production costs. Operating expenses were slightly higher due to increased investment in marketing and R&D, but this was expected as we continue to expand our product portfolio. We also saw a significant increase in new customer acquisitions, which contributed to the growth in both revenue and market share. The company's international presence continues to expand, with sales in Europe and Asia growing by 20% year-over-year. Despite the positive results, we remain cautious about the global economic uncertainty and the potential impact of inflation on consumer spending. Looking ahead, we are focusing on further improving operational efficiency and driving innovation in product development. Our outlook for the rest of the year is positive, with expectations of continued growth across all regions. We are also investing in sustainable business practices to reduce our environmental impact and ensure long-term profitability. As we move into the second quarter, we will be closely monitoring market trends and adjusting our strategy accordingly to remain competitive in the evolving industry landscape. The board of directors is confident in the company's ability to meet its financial goals for 2025 and beyond. We remain committed to delivering value to our shareholders while maintaining a strong focus on customer satisfaction and employee well-being. In conclusion, the first quarter of 2025 has been a strong start to the year, and we are optimistic about the future.",
# }


@app.get(
    path="/get/{id}",
    summary="Get note by ID",
    description="<h1>Fetches a note from the database based on the provided ID.</h1>",
)
async def get_note_by_id(id: int, session: SessionDepends):
    return await ApiHelper.get_note_by_id(id=id, session=session)


@app.get(
    path="/get",
    summary="Get all notes",
    description="<h1>Fetches all notes stored in the database.</h1>",
)
async def get_all_notes(session: SessionDepends):
    return await ApiHelper.get_all_notes(session=session)


@app.put(
    path="/update/{id}",
    summary="Update a note",
    description="<h1>Updates an existing note in the database based on the provided ID and data.</h1>",
)
async def update_note(id: int, data: NotePutSchema, session: SessionDepends):
    return await ApiHelper.update_note(id=id, session=session, data=data)


@app.delete(
    path="/delete/{id}",
    summary="Delete a note",
    description="<h1>Deletes a note from the database based on the provided ID.</h1>",
)
async def delete_note(id: int, session: SessionDepends):
    return await ApiHelper.delete_note(id=id, session=session)


@app.get("/analytic/total_words")
async def total_words(session: SessionDepends):
    return await ApiHelper.get_total_word_count(session=session)


@app.get("/analytic/length")
async def length(session: SessionDepends):
    return await ApiHelper.get_average_note_length(session=session)


@app.get("/analytic/common_words")
async def common_words(session: SessionDepends, min_count: int = 3):
    return await ApiHelper.get_most_common_words(session=session, min_count=min_count)


@app.get("/analytic/longest")
async def longest(session: SessionDepends, top_n: int = 3):
    return await ApiHelper.get_longest_notes(session=session, top_n=top_n)


@app.get("/analytic/shortest")
async def shortest(session: SessionDepends, top_n: int = 3):
    return await ApiHelper.get_shortest_notes(session=session, top_n=top_n)
