# LLM-Generated: validation exceptions for payload and model contract checks.

from .base import ValidationError


class PayloadValidationError(ValidationError):
    """Raised when a JSON payload is missing required data."""


class ModelValidationError(ValidationError):
    """Raised when a model instance fails invariants."""


__all__ = ["ModelValidationError", "PayloadValidationError", "ValidationError"]
