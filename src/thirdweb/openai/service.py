from typing import Optional

from httpx import AsyncClient, Response, Timeout


class OpenAIService:
    """
    OpenAIService class that communicates with the OpenAI API to send and receive chat completions.
    """

    BASE_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self.model = model

    def _prepare_headers(self) -> dict:
        """
        Prepare the necessary headers for the API request, including the authorization token.

        :returns: A dictionary containing the headers required for the API request.
        :rtype: dict
        """
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _prepare_request_payload(self, user_prompt: str) -> dict:
        """
        Prepare the request payload for the AI API, including the model and the user-provided prompt.

        :param user_prompt: The input prompt provided by the user to be sent to the AI.
        :type user_prompt: str
        :returns: A dictionary containing the request payload to be sent to the API.
        :rtype: dict
        """
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": user_prompt}],
        }

    async def _send_request(self, request_data: dict, headers: dict) -> Response:
        """
        Send an HTTP POST request to the AI API with the provided data and headers.

        :param request_data: The data to be sent in the request body.
        :type request_data: dict
        :param headers: The headers to be included in the request.
        :type headers: dict
        :returns: The response object returned by the AI API.
        :rtype: Response
        """
        async with AsyncClient() as client:
            timeout = Timeout(10.0)
            return await client.post(
                self.BASE_URL, json=request_data, headers=headers, timeout=timeout
            )

    async def get_response(self, user_prompt: str) -> Response:
        """
        Prepare the request, send it to the AI service, and return the response.

        :param user_prompt: The input prompt to be sent to the AI service.
        :type user_prompt: str
        :returns: The response object returned by the AI API.
        :rtype: Response
        """
        headers = self._prepare_headers()
        request_data = self._prepare_request_payload(user_prompt=user_prompt)
        return await self._send_request(request_data=request_data, headers=headers)

    async def fetch_data(self, user_prompt: str) -> Optional[str]:
        """
        Main method to fetch data from the AI API based on the user's prompt.

        :param user_prompt: The input provided by the user.
        :type user_prompt: str
        :returns: The AI-generated response, or None if the request fails.
        :rtype: Optional[str]
        """
        response = await self.get_response(user_prompt=user_prompt)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return None
