# LLM-Generated: stable service entrypoint for the character-import workflow.

from __future__ import annotations

from typing import Any

from ..client.http_client import AlchemyHTTPClient
from ..errors.validation import PayloadValidationError
from ..models.character import Character
from ..schemas.character_import import character_from_api, character_to_api, validate_character_payload


class CharacterService:
    def __init__(self, client: AlchemyHTTPClient | None = None, *, endpoint: str = "/api/characters/import"):
        self.client = client or AlchemyHTTPClient(base_url="https://example.com")
        self.endpoint = endpoint

    def build_payload(self, character: Character | dict[str, Any]) -> dict[str, Any]:
        if isinstance(character, Character):
            payload = character_to_api(character)
        elif isinstance(character, dict):
            payload = dict(character)
        else:
            raise TypeError("character must be a Character instance or a payload dict")

        validate_character_payload(payload)
        return payload

    def import_character(self, character: Character | dict[str, Any]) -> Any:
        payload = self.build_payload(character)
        return self.client.post_json(self.endpoint, payload)

    def import_character_payload(self, payload: dict[str, Any]) -> Any:
        validated = validate_character_payload(payload)
        return self.client.post_json(self.endpoint, validated)

    def parse_character(self, payload: dict[str, Any]) -> Character:
        if not isinstance(payload, dict):
            raise TypeError("Character payload must be a dict")
        try:
            return character_from_api(payload)
        except Exception as exc:  # pragma: no cover - re-raised as validation contract failure
            raise PayloadValidationError(str(exc)) from exc

    def export_character(self, character: Character) -> dict[str, Any]:
        return character_to_api(character)
