# LLM-Generated: HTTP-specific exceptions for the character import workflow.

from .base import AlchemyPyError, AuthenticationError, ClientError, RequestError


class APIError(RequestError):
    """Raised when the API responds with an error status code."""

    def __init__(self, message: str, status_code: int | None = None, response_text: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class RateLimitError(APIError):
    """Raised when the API limits a request."""


class NotFoundError(APIError):
    """Raised when an endpoint cannot be found."""


class BadRequestError(APIError):
    """Raised when the API rejects the request body."""


__all__ = [
    "AlchemyPyError",
    "APIError",
    "AuthenticationError",
    "BadRequestError",
    "ClientError",
    "NotFoundError",
    "RateLimitError",
    "RequestError",
]
