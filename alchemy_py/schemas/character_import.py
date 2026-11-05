from __future__ import annotations

from typing import Any

from ..models.ability_score import AbilityScore
from ..models.action import (
    ActionStep,
    ActionStepAttack,
    ActionStepDamage,
    ActionStepJournalCommand,
    ActionStepSkillCheck,
    ActionStepType,
    ActionType,
    Command,
    RollModifier,
)
from ..models.alignment import Alignment, Morality, Order
from ..models.character import Character


class CharacterImportValidator:
    required_fields = {
        "abilityScores",
        "alignment",
        "currentHP",
        "maxHP",
        "name",
    }

    @staticmethod
    def validate(payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise TypeError("Character import payload must be a dict")

        missing = sorted(CharacterImportValidator.required_fields - set(payload.keys()))
        if missing:
            raise ValueError(f"Character payload missing required fields: {missing}")

        if not isinstance(payload["abilityScores"], list):
            raise TypeError("abilityScores must be a list")
        if not isinstance(payload["name"], str):
            raise TypeError("name must be a string")
        if not isinstance(payload["currentHP"], int):
            raise TypeError("currentHP must be an integer")
        if not isinstance(payload["maxHP"], int):
            raise TypeError("maxHP must be an integer")
        if not isinstance(payload["alignment"], str):
            raise TypeError("alignment must be a string")

        return payload


def validate_character_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return CharacterImportValidator.validate(payload)


def ability_score_from_api(data: dict[str, Any]) -> AbilityScore:
    if not isinstance(data, dict):
        raise TypeError("ability score payload must be a dict")
    return AbilityScore(name=str(data["name"]), score=int(data["value"]))


def ability_score_to_api(score: AbilityScore) -> dict[str, Any]:
    return {"name": score.name, "value": score.score}


def alignment_from_api(value: str | None) -> Alignment | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("alignment must be a string or None")

    token_map = {
        "good": Morality.Good,
        "neutral": Morality.Neutral,
        "evil": Morality.Evil,
        "lawful": Order.Lawful,
        "chaotic": Order.Chaotic,
    }
    text = value.strip()
    if text.lower() == "any alignment":
        return None

    parts = text.split()
    if len(parts) == 2:
        order_text = parts[0].lower()
        morality_text = parts[1].lower()
        if order_text in {"lawful", "neutral", "chaotic"} and morality_text in {"good", "neutral", "evil"}:
            return Alignment(morality=Morality(morality_text.title()), order=Order(order_text.title()))
        return None

    if text.lower() in {"good", "neutral", "evil"}:
        return Alignment(morality=Morality(text.title()), order=Order.Neutral)

    if text.lower() in {"lawful", "chaotic"}:
        return Alignment(morality=Morality.Neutral, order=Order(text.title()))

    return None


def alignment_to_api(alignment: Alignment | None) -> str:
    if alignment is None:
        return "Any Alignment"
    return str(alignment)


def saving_throw_from_api(data: dict[str, Any] | None) -> dict[str, Any] | None:
    if data is None:
        return None
    if not isinstance(data, dict):
        raise TypeError("savingThrow payload must be a dict or None")
    return {"abilityName": data.get("abilityName"), "difficultyClass": data.get("difficultyClass", 0)}


def saving_throw_to_api(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {}
    return payload


def action_damage_from_api(data: dict[str, Any]) -> ActionStepDamage:
    if not isinstance(data, dict):
        raise TypeError("damageRolls entry must be a dict")
    dice_value = data.get("dice")
    if dice_value is None:
        raise ValueError("damageRolls entry must contain a dice value")
    return ActionStepDamage(
        abilityName=data.get("abilityName", ""),
        bonus_or_dice=dice_value,
        dice=data.get("type"),
    )


def action_damage_to_api(damage: ActionStepDamage) -> dict[str, Any]:
    return {
        "abilityName": damage.abilityName,
        "dice": str(damage.dice),
        "type": damage.type,
    }


def action_attack_from_api(data: dict[str, Any]) -> ActionStepAttack:
    if not isinstance(data, dict):
        raise TypeError("attack payload must be a dict")
    return ActionStepAttack(
        ability=data.get("ability", ""),
        actionType=data.get("actionType", ActionType.Action),
        crit=int(data.get("crit", 20)),
        damageRolls=[action_damage_from_api(item) for item in data.get("damageRolls", [])],
        isProficient=bool(data.get("isProficient", False)),
        isRanged=bool(data.get("isRanged", False)),
        name=data.get("name", ""),
        range_=data.get("range"),
        longRange=data.get("longRange"),
        rollsAttack=bool(data.get("rollsAttack", True)),
        savingThrow=saving_throw_from_api(data.get("savingThrow")),
    )


def action_attack_to_api(attack: ActionStepAttack) -> dict[str, Any]:
    payload = {
        "ability": attack.ability,
        "actionType": attack.actionType.value if hasattr(attack.actionType, "value") else str(attack.actionType),
        "crit": attack.crit,
        "damageRolls": [action_damage_to_api(item) for item in attack.damageRolls],
        "isProficient": attack.isProficient,
        "isRanged": attack.isRanged,
        "name": attack.name,
        "rollsAttack": attack.rollsAttack,
        "savingThrow": saving_throw_to_api(attack.savingThrow),
    }
    if attack.range is not None:
        payload["range"] = attack.range
    if attack.longRange is not None:
        payload["longRange"] = attack.longRange
    return payload


def action_step_from_api(data: dict[str, Any]) -> ActionStep:
    if not isinstance(data, dict):
        raise TypeError("action step payload must be a dict")

    step_type = data.get("type")
    kwargs = {"type": ActionStepType(step_type)} if step_type is not None else {}

    if "attack" in data and data["attack"] not in (None, {}):
        kwargs["attack"] = action_attack_from_api(data["attack"])
    if "journalCommand" in data and data["journalCommand"] not in (None, {}):
        kwargs["journalCommand"] = ActionStepJournalCommand(Command.Me, "")
    if "skillCheck" in data and data["skillCheck"] not in (None, {}):
        kwargs["skillCheck"] = ActionStepSkillCheck(RollModifier.Advantage, "")

    return ActionStep(**kwargs)


def action_step_to_api(step: ActionStep) -> dict[str, Any]:
    payload: dict[str, Any] = {"type": step.type.value if hasattr(step.type, "value") else str(step.type)}
    if step.attack is not None:
        payload["attack"] = action_attack_to_api(step.attack)
    if step.journalCommand is not None:
        payload["journalCommand"] = {"command": step.journalCommand.command.value if hasattr(step.journalCommand.command, "value") else str(step.journalCommand.command), "args": step.journalCommand.args}
    if step.skillCheck is not None:
        payload["skillCheck"] = {"rollModifier": step.skillCheck.rollModifier.value if hasattr(step.skillCheck.rollModifier, "value") else str(step.skillCheck.rollModifier), "skillName": step.skillCheck.skillName}
    return payload


def character_from_api(payload: dict[str, Any]) -> Character:
    validate_character_payload(payload)
    ability_scores = [ability_score_from_api(item) for item in payload["abilityScores"]]
    alignment = alignment_from_api(payload.get("alignment"))
    return Character(
        name=str(payload.get("name", "")),
        abilityScores=ability_scores,
        alignment=alignment,
        currentHP=int(payload.get("currentHP", 0)),
        maxHP=int(payload.get("maxHP", 0)),
        exp=int(payload.get("exp", 0)),
        initiativeBonus=int(payload.get("initiativeBonus", 0)),
        imageURL=payload.get("imageURL"),
        isNPC=bool(payload.get("isNPC", False)),
        isSpellcaster=bool(payload.get("isSpellcaster", False)),
        speed=int(payload.get("speed", 0)),
        type=str(payload.get("type", "")),
    )


def character_to_api(character: Character) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "abilityScores": [ability_score_to_api(item) for item in character.abilityScores],
        "alignment": alignment_to_api(character.alignment),
        "currentHP": character.currentHP,
        "maxHP": character.maxHP,
        "name": character.name,
    }
    if character.exp is not None:
        payload["exp"] = character.exp
    if character.initiativeBonus:
        payload["initiativeBonus"] = character.initiativeBonus
    if character.imageURL:
        payload["imageURL"] = character.imageURL
    if character.isNPC:
        payload["isNPC"] = True
    if character.isSpellcaster:
        payload["isSpellcaster"] = True
    if character.speed:
        payload["speed"] = character.speed
    if character.type:
        payload["type"] = character.type
    return payload
