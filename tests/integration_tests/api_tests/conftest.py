import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.backend.api import app
from src.database.database.models import Base, NoteModel, NoteVersionModel
from src.database.session import engine

# To ensure optimal performance, please avoid running all test functions simultaneously.
# The free-tier of ChatGPT has limitations in handling data summarization.
# Please execute separately.


@pytest_asyncio.fixture(scope="session")
async def client():
    """Creates an asynchronous test client for FastAPI using ASGITransport.

    This fixture provides a shared test client instance for all tests within the session scope.
    It allows making HTTP requests to the FastAPI application.
    """
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    """Resets the database before each test function.

    This fixture automatically drops and recreates the specified database tables
    before each test to ensure a clean state and avoid data persistence issues.
    """
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.drop_all,
            tables=[NoteModel.__table__, NoteVersionModel.__table__],
        )
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[NoteModel.__table__, NoteVersionModel.__table__],
        )


@pytest_asyncio.fixture
async def id(client):
    """Creates a test note and returns its ID.

    This fixture sends a POST request to create a note in the database
    and returns the generated note ID for use in tests.
    """
    response = await client.post(
        url="/crud/post",
        json={"title": "Project Update: March 2025", "content": "Test content!"},
    )
    return response.json()["note_id"]


@pytest.fixture
async def prepare_data(client):
    """Prepares test data by creating multiple notes.

    This fixture populates the database with sample notes to facilitate
    testing features like analytics and retrieval.
    """
    await client.post(
        url="/crud/post",
        json={
            "title": "Short",
            "content": "Tiny Note, Note"
        }
    )
    await client.post(
        url="/crud/post",
        json={
            "title": "Long",
            "content": "Not Tiny, but a much longer Note Note. woah longer"
        }
    )
