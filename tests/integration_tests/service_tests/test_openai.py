import pytest
from httpx import Response

from src.thirdweb.openai.service import OpenAIService
from tests.integration_tests.conftest import openai_skip_send_request, openai_skip_get_request


# ----------------------------SEND REQUEST----------------------------------------------------
@pytest.mark.skipif(openai_skip_send_request, reason="The flag 'openai_skip_send_request' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_send_request(mock_post):
    """Test the 'fetch_data' method of OpenAIService class"""

    service = OpenAIService(api_key="test_api_key", model="gpt-3.5-turbo")
    user_prompt = "Explain SOLID principles"
    result = await service.fetch_data(user_prompt=user_prompt)

    assert result == "AI response"


@pytest.mark.skipif(openai_skip_send_request, reason="The flag 'openai_skip_send_request' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_send_request_error(mock_post, monkeypatch):
    """Test the 'fetch_data' method of OpenAIService class for error handling."""

    service = OpenAIService(api_key="test_api_key", model="gpt-3.5-turbo")
    user_prompt = "Explain SOLID principles"

    async def mock_post_error(self, url, **kwargs):
        return Response(status_code=400, json={"error": "Bad request"})

    monkeypatch.setattr("httpx.AsyncClient.post", mock_post_error)
    result = await service.fetch_data(user_prompt=user_prompt)

    assert result is None
# ----------------------------SEND REQUEST----------------------------------------------------


# ----------------------------GET RESPONSE----------------------------------------------------
@pytest.mark.skipif(openai_skip_get_request, reason="The flag 'openai_skip_get_request' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_response(mock_post):
    """Test the 'get_response' method of OpenAIService class."""

    service = OpenAIService(api_key="test_api_key", model="gpt-3.5-turbo")
    user_prompt = "What's the weather today?"
    response = await service.get_response(user_prompt=user_prompt)

    assert response.status_code == 200
    assert response.json() == {"choices": [{"message": {"content": "AI response"}}]}
# ----------------------------GET RESPONSE----------------------------------------------------