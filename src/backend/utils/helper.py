import asyncio
from typing import Optional, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.backend.utils.exceptions import NotFoundError
from src.config import env_config
from src.backend.utils.decorator import handle_exceptions
from src.backend.utils.schemas import NotePutSchema, NoteGetSchemaResponse
from src.database.database.models import Base
from src.database.database.queries import NoteQuery
from src.thirdweb.analytic.service import NoteAnalyticsService
from src.thirdweb.openai.service import OpenAIService
from src.thirdweb.openai.utils import PromptUtils


class ApiHelper:
    @staticmethod
    @handle_exceptions
    async def create_note(data: dict, session: AsyncSession) -> JSONResponse:
        """Creates a new note with AI-generated summarization."""
        ai_service = OpenAIService(
            model=env_config.OPENAI_MODEL,
            api_key=env_config.OPENAI_API_KEY,
        )
        prompt = PromptUtils.create_prompt_for_summarization(text=data["content"])
        data["summarization"] = await asyncio.create_task(ai_service.fetch_data(prompt))

        repo = NoteQuery(session)
        id = await repo.create(data)

        return ApiHelper._success_response(status_code=201, content={"note_id": id})

    @staticmethod
    @handle_exceptions
    async def get_note_by_id(id: int, session: AsyncSession) -> JSONResponse:
        """Retrieves a note by its ID."""
        note = await ApiHelper._fetch_note_by_id(id, session)
        validated_note = NoteGetSchemaResponse.model_validate(jsonable_encoder(note))

        return ApiHelper._success_response(
            status_code=200, content=validated_note.model_dump()
        )

    @staticmethod
    @handle_exceptions
    async def get_all_notes(session: AsyncSession) -> JSONResponse:
        """Retrieves all notes."""
        notes = await ApiHelper._fetch_all_notes(session)
        return ApiHelper._success_response(status_code=200, content=notes)

    @staticmethod
    @handle_exceptions
    async def update_note(
        id: int, session: AsyncSession, data: NotePutSchema
    ) -> JSONResponse:
        """Updates a note."""
        repo = NoteQuery(session)
        note = await ApiHelper._fetch_note_by_id(id, session)
        updated_data = data.model_dump(exclude_unset=True)
        await repo.put(obj=note, data=updated_data)

        return ApiHelper._success_response(status_code=204)

    @staticmethod
    @handle_exceptions
    async def delete_note(id: int, session: AsyncSession) -> JSONResponse:
        """Deletes a note."""
        repo = NoteQuery(session)
        note = await ApiHelper._fetch_note_by_id(id, session)
        await repo.delete(note)

        return ApiHelper._success_response(status_code=204)

    @staticmethod
    async def get_total_word_count(session: AsyncSession) -> JSONResponse:
        """Returns the total word count across all notes."""
        notes = await ApiHelper._fetch_all_notes(session)
        analytics = NoteAnalyticsService(notes=notes)
        word_count = analytics.get_total_word_count()

        return ApiHelper._success_response(status_code=200, content=int(word_count))

    @staticmethod
    async def get_average_note_length(session: AsyncSession) -> JSONResponse:
        """Returns the average note length."""
        notes = await ApiHelper._fetch_all_notes(session)
        analytics = NoteAnalyticsService(notes=notes)
        avg_length = analytics.get_average_note_length()

        return ApiHelper._success_response(status_code=200, content=float(avg_length))

    @staticmethod
    async def get_most_common_words(
        min_count: int, session: AsyncSession
    ) -> JSONResponse:
        """Returns the most common words across all notes."""
        notes = await ApiHelper._fetch_all_notes(session)
        analytics = NoteAnalyticsService(notes=notes)
        common_words = analytics.get_most_common_words(min_count=min_count)

        return ApiHelper._success_response(status_code=200, content=common_words)

    @staticmethod
    async def get_longest_notes(top_n: int, session: AsyncSession) -> JSONResponse:
        """Returns the longest notes."""
        notes = await ApiHelper._fetch_all_notes(session)
        analytics = NoteAnalyticsService(notes=notes)
        longest_notes = analytics.get_longest_notes(top_n=top_n)

        return ApiHelper._success_response(status_code=200, content=longest_notes)

    @staticmethod
    async def get_shortest_notes(top_n: int, session: AsyncSession) -> JSONResponse:
        """Returns the shortest notes."""
        notes = await ApiHelper._fetch_all_notes(session)
        analytics = NoteAnalyticsService(notes=notes)
        shortest_notes = analytics.get_shortest_notes(top_n=top_n)

        return ApiHelper._success_response(status_code=200, content=shortest_notes)

    @staticmethod
    async def _fetch_all_notes(session: AsyncSession) -> list[dict]:
        """Helper method to retrieve all notes and validate them."""
        repo = NoteQuery(session)
        notes = await repo.get_all()
        if not notes:
            raise NotFoundError(
                "Note is not found. The provided ID may be incorrect, or no data is available."
            )

        validated_notes = [
            NoteGetSchemaResponse.model_validate(jsonable_encoder(note))
            for note in notes
        ]
        return [note.model_dump() for note in validated_notes]

    @staticmethod
    @handle_exceptions
    async def _fetch_note_by_id(id: int, session: AsyncSession) -> Optional[Base]:
        """Helper method to get a note by ID or raise a 404 response."""
        repo = NoteQuery(session)
        note = await repo.get_by_id(id)
        if not note:
            raise NotFoundError(
                "Note is not found. The provided ID may be incorrect, or no data is available."
            )
        return note

    @staticmethod
    def _success_response(
        status_code: int, content: Optional[Any] = None
    ) -> JSONResponse:
        """Creates a standardized JSON response."""
        return JSONResponse(status_code=status_code, content=content)
