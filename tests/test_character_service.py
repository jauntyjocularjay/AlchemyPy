import json
from pathlib import Path

import pytest

from alchemy_py.client import AlchemyHTTPClient
from alchemy_py.errors import PayloadValidationError
from alchemy_py.models.ability_score import AbilityScore
from alchemy_py.models.alignment import Alignment, Morality, Order
from alchemy_py.models.character import Character
from alchemy_py.services.character_service import CharacterService


@pytest.fixture
def example_character():
    return Character(
        name="Guard",
        abilityScores=[AbilityScore("str", 16), AbilityScore("dex", 14)],
        alignment=Alignment(Morality.Good, Order.Lawful),
        currentHP=18,
        maxHP=18,
        isNPC=True,
        type="Humanoid",
    )


def test_character_service_builds_valid_export_payload(example_character):
    service = CharacterService(client=AlchemyHTTPClient(base_url="https://example.com"))

    payload = service.build_payload(example_character)

    assert payload["name"] == "Guard"
    assert payload["alignment"] == "Lawful Good"
    assert payload["abilityScores"][0] == {"name": "str", "value": 16}
    assert payload["currentHP"] == 18
    assert payload["maxHP"] == 18


def test_character_service_import_character_uses_client(example_character, monkeypatch):
    service = CharacterService(client=AlchemyHTTPClient(base_url="https://example.com"))
    calls = {}

    def fake_post_json(path, payload):
        calls["path"] = path
        calls["payload"] = payload
        return {"status": "ok", "payload": payload}

    monkeypatch.setattr(service.client, "post_json", fake_post_json)

    result = service.import_character(example_character)

    assert result["status"] == "ok"
    assert calls["payload"]["name"] == "Guard"
    assert calls["path"] == "/api/characters/import"


def test_character_service_rejects_invalid_payload():
    service = CharacterService(client=AlchemyHTTPClient(base_url="https://example.com"))

    with pytest.raises(Exception):
        service.import_character_payload({"name": "No scores here"})


def test_client_auth_headers_include_bearer_token():
    client = AlchemyHTTPClient(base_url="https://example.com", api_key="abc123")

    assert client.headers["Authorization"] == "Bearer abc123"
    assert client.headers["Content-Type"] == "application/json"
