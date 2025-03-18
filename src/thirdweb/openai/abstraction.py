from abc import ABC, abstractmethod
from typing import Optional

from httpx import Response


class AIService(ABC):
    """
    Abstract base class representing a general AI service. It defines the interface for interacting
    with an AI API, including preparing headers, request payloads, sending requests, and handling responses.

    Subclasses should implement the required methods to communicate with specific AI services.
    """

    BASE_URL = ...

    def __init__(self, model: str, api_key: str):
        """
        Initialize the AIService with the model and API key.

        :param model: The AI model to be used (e.g., "gpt-3.5-turbo").
        :type model: str
        :param api_key: The API key for authenticating requests to the AI service.
        :type api_key: str
        """
        self.model = model
        self._api_key = api_key

    @abstractmethod
    def _prepare_headers(self) -> dict:
        """
        Prepare the necessary headers for the API request, including the authorization token.

        :returns: A dictionary containing the headers required for the API request.
        :rtype: dict
        """
        ...

    @abstractmethod
    def _prepare_request_payload(self, user_prompt: str) -> dict:
        """
        Prepare the request payload for the AI API, including the model and the user-provided prompt.

        :param user_prompt: The input prompt provided by the user to be sent to the AI.
        :type user_prompt: str
        :returns: A dictionary containing the request payload to be sent to the API.
        :rtype: dict
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    async def get_response(self, user_prompt: str) -> Response:
        """
        Prepare the request, send it to the AI service, and return the response.

        :param user_prompt: The input prompt to be sent to the AI service.
        :type user_prompt: str
        :returns: The response object returned by the AI API.
        :rtype: Response
        """
        ...

    @abstractmethod
    async def fetch_data(self, user_prompt: str) -> Optional[str]:
        """
        Main method to fetch data from the AI API based on the user's prompt.

        :param user_prompt: The input provided by the user.
        :type user_prompt: str
        :returns: The AI-generated response, or None if the request fails.
        :rtype: Optional[str]
        """
        ...
