from typing import Optional, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.config import env_config
from src.backend.utils.decorator import handle_exceptions
from src.backend.utils.schemas import (
    NotePutSchema,
    NoteGetSchemaResponse,
)
from src.database.database.models import Base
from src.database.database.queries import NoteQuery
from src.thirdweb.service import OpenAIService
from src.thirdweb.utils import PromptUtils


class ApiHelper:
    @staticmethod
    @handle_exceptions
    async def create(data: dict, session: AsyncSession):
        ai_service = OpenAIService(
            model=env_config.OPENAI_MODEL,
            api_key=env_config.OPENAI_API_KEY,
        )
        prompt = PromptUtils.create_prompt_for_summarization(text=data["content"])
        data["summarization"] = await ai_service.fetch_data(prompt)
        print(data)
        repo = NoteQuery(session)
        obj_id = await repo.create(data)
        return ApiHelper.success(status_code=201, content={"object id": obj_id})

    @staticmethod
    @handle_exceptions
    async def get_by_id(id: int, session: AsyncSession):
        repo = NoteQuery(session)
        obj = await repo.get_by_id(id)
        obj_dict = jsonable_encoder(obj)
        validated_obj = NoteGetSchemaResponse.model_validate(obj_dict)
        return ApiHelper.success(
            status_code=200,
            content=validated_obj.model_dump(),
        )

    @staticmethod
    @handle_exceptions
    async def get_all(session: AsyncSession):
        repo = NoteQuery(session)
        objs = await repo.get_all()

        objs_dict = [jsonable_encoder(obj) for obj in objs]
        validated_objs = [
            NoteGetSchemaResponse.model_validate(obj) for obj in objs_dict
        ]
        transformed_objs = [
            NoteGetSchemaResponse.model_dump(obj) for obj in validated_objs
        ]
        return ApiHelper.success(status_code=200, content=transformed_objs)

    @staticmethod
    @handle_exceptions
    async def put(obj: Base, session: AsyncSession, data: NotePutSchema):
        repo = NoteQuery(session)
        data_wo_none = data.model_dump(exclude_unset=True)
        await repo.put(obj=obj, data=data_wo_none)
        return ApiHelper.success(status_code=204)

    @staticmethod
    @handle_exceptions
    async def delete(obj: Base, session: AsyncSession):
        repo = NoteQuery(session)
        await repo.delete(obj)
        return ApiHelper.success(status_code=204)

    @staticmethod
    def success(status_code: int, content: Optional[Any] = None) -> JSONResponse:
        return JSONResponse(status_code=status_code, content=content)
