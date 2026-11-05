import json
from pathlib import Path

import pytest

from alchemy_py.models.character import Character
from alchemy_py.schemas.character_import import (
    action_step_from_api,
    action_step_to_api,
    character_from_api,
    character_to_api,
    validate_character_payload,
)


@pytest.fixture
def character_payload():
    path = Path(__file__).resolve().parents[1] / "API-JSON" / "character.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_character_import_from_api_parses_documented_shape(character_payload):
    character = character_from_api(character_payload)

    assert isinstance(character, Character)
    assert character.name == "Guard"
    assert character.abilityScores[0].name == "str"
    assert character.abilityScores[0].score == 16
    assert character.currentHP == 18
    assert str(character.alignment) == "Lawful Good"
    assert character.maxHP == 18


def test_character_import_round_trip_preserves_core_fields(character_payload):
    character = character_from_api(character_payload)
    payload = character_to_api(character)

    assert payload["name"] == "Guard"
    assert payload["alignment"] == "Lawful Good"
    assert payload["abilityScores"][0] == {"name": "str", "value": 16}
    assert payload["currentHP"] == 18
    assert payload["maxHP"] == 18


def test_character_import_validator_rejects_missing_required_fields():
    with pytest.raises(ValueError):
        validate_character_payload({"name": "Guard"})


def test_action_step_round_trip_matches_api_shape(character_payload):
    step_payload = character_payload["actions"][0]["steps"][0]
    step = action_step_from_api(step_payload)
    converted = action_step_to_api(step)

    assert converted["type"] == "custom-attack"
    assert converted["attack"]["ability"] == "str"
    assert converted["attack"]["damageRolls"][0]["dice"] == "1d8"
