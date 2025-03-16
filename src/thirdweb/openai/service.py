from typing import Optional

from httpx import AsyncClient, Response, Timeout

from src.thirdweb.openai.abstraction import AIService


class OpenAIService(AIService):
    """
    OpenAIService class that communicates with the OpenAI API to send and receive chat completions.
    """

    BASE_URL = "https://api.openai.com/v1/chat/completions"

    def _prepare_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _prepare_request_payload(self, user_prompt: str) -> dict:
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": user_prompt}],
        }

    async def _send_request(self, request_data: dict, headers: dict) -> Response:
        async with AsyncClient() as client:
            timeout = Timeout(10.0)
            return await client.post(
                self.BASE_URL, json=request_data, headers=headers, timeout=timeout
            )

    async def _get_response(self, user_prompt: str) -> Response:
        headers = self._prepare_headers()
        request_data = self._prepare_request_payload(user_prompt=user_prompt)
        return await self._send_request(request_data=request_data, headers=headers)

    async def fetch_data(self, user_prompt: str) -> Optional[str]:
        response = await self._get_response(user_prompt=user_prompt)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            # own problem
            return None
