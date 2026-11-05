# LLM-Generated: typed project exceptions for model validation and API failures.


class AlchemyPyError(Exception):
    """Base exception for all AlchemyPy failures."""


class ValidationError(AlchemyPyError):
    """Raised when a model or payload is invalid."""


class ClientError(AlchemyPyError):
    """Raised for generic client-side errors."""


class RequestError(ClientError):
    """Raised when an HTTP request fails."""


class AuthenticationError(ClientError):
    """Raised when the API rejects authentication."""
