import pytest
from httpx import Response


@pytest.fixture
def mock_post(monkeypatch):
    """
    Mocking POST request httpx AsyncClient, to stimulate APIs response.
    """
    async def mock_post_response(self, url, **kwargs):
        json = kwargs.get("json", None)

        if url == "https://api.openai.com/v1/chat/completions":
            if json and "messages" in json:
                return Response(
                    status_code=200,
                    json={"choices": [{"message": {"content": "AI response"}}]},
                )
            return Response(
                status_code=400,
                json={"error": "Bad request"}
            )
        return Response(
            status_code=404,
            json={"error": "Not Found"}
        )

    monkeypatch.setattr("httpx.AsyncClient.post", mock_post_response)