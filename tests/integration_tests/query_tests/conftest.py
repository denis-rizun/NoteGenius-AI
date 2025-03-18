import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import env_config
from src.database.database.models import Base, NoteModel, NoteVersionModel
from src.database.database.queries import NoteQuery

engine = create_async_engine(env_config.TEST_DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
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

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session():
    """
    Fixture to create and provide a database session for each test function.

    This fixture establishes a new session for each test case using
    the async_session context manager. The session is yielded to the
    test function and automatically closed after the test completes.

    Returns:
        AsyncSession: A session object for interacting with the database.
    """
    async with async_session() as session:
        yield session


@pytest.fixture
async def create_data(session):
    """
    Fixture to create a set of sample notes in the database for testing.

    This fixture uses the provided `session` to create multiple note
    entries in the database. It then returns a list of dictionaries
    containing the note data

    Args:
        session (AsyncSession): The database session to interact with the database.

    Returns:
        list[dict]: A list of dictionaries representing the created notes,
                    each containing the 'id', 'title', 'content',
                    'summarization', and 'version_number'.
    """
    notes = [
        {
        "title": "Project Update: March 2025",
        "content": "Today, we successfully integrated the new recommendation engine.",
        "summarization": "Integration of AI recommendation engine completed.",
        "version_number": 1,
        },
        {
        "title": "Project Delete: June 1515",
        "content": "Tomorrow, the project's going to be deleted",
        "summarization": "They want to delete project tomorrow",
        "version_number": 1,
        }
    ]
    repo = NoteQuery(session)
    for note in notes:
        note_id = await repo.create(note)
        note["id"] = note_id

    return notes

@pytest.fixture
def note_repo(session):
    """Fixture for NoteQuery, providing a reusable instance."""
    return NoteQuery(session)
