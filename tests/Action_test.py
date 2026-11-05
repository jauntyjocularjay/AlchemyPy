import pytest

from Action import (
    Action,
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
from Dice import Dice

# LLM-Generated: Tests cover the legacy action payload contract used by the Alchemy import format.


def test_action_step_damage_parses_string_dice_and_keeps_api_fields():
    damage = ActionStepDamage("str", "4d6", "Slashing")

    assert damage.abilityName == "str"
    assert damage.bonus == 0
    assert isinstance(damage.dice, Dice)
    assert str(damage.dice) == "4d6"
    assert damage.type == "Slashing"


def test_action_step_damage_accepts_bonus_and_dice_object():
    damage = ActionStepDamage("dex", 2, Dice("1d8"), "Piercing")

    assert damage.abilityName == "dex"
    assert damage.bonus == 2
    assert isinstance(damage.dice, Dice)
    assert str(damage.dice) == "1d8"
    assert damage.type == "Piercing"


def test_action_step_accepts_custom_attack_payload_shape():
    attack = ActionStepAttack(
        ability="str",
        actionType=ActionType.Action,
        crit=20,
        damageRolls=[ActionStepDamage("str", "1d8", "Slashing")],
        isProficient=True,
        isRanged=False,
        name="Slam",
        rollsAttack=True,
        savingThrow={},
    )
    step = ActionStep(type=ActionStepType.CustomAttack, attack=attack)

    assert step.type is ActionStepType.CustomAttack
    assert step.attack is attack
    assert step.attack.damageRolls[0].abilityName == "str"


def test_action_step_rejects_missing_payload():
    with pytest.raises(ValueError):
        ActionStep(type=ActionStepType.CustomAttack)


def test_action_step_rejects_invalid_payload_type():
    with pytest.raises(TypeError):
        ActionStep(type=ActionStepType.CustomAttack, skillCheck="not-a-skill-check")


def test_action_parses_api_payload_and_serializes_round_trip():
    payload = {
        "description": "Melee Weapon Attack: +5 to hit.",
        "name": "Longsword",
        "sortOrder": 0,
        "steps": [
            {
                "attack": {
                    "ability": "str",
                    "actionType": "Action",
                    "crit": 20,
                    "damageRolls": [{"abilityName": "str", "dice": "1d8", "type": "Piercing"}],
                    "isProficient": True,
                    "isRanged": False,
                    "name": "Longsword",
                    "rollsAttack": True,
                    "savingThrow": {},
                },
                "type": "custom-attack",
            }
        ],
    }

    action = Action.from_api(payload)
    round_trip = action.to_api()

    assert action.name == "Longsword"
    assert action.steps[0].type is ActionStepType.CustomAttack
    assert action.steps[0].attack.name == "Longsword"
    assert round_trip["steps"][0]["type"] == "custom-attack"
    assert round_trip["steps"][0]["attack"]["damageRolls"][0]["dice"] == "1d8"


def test_action_step_accepts_string_aliases_for_commands_and_skill_checks():
    command = ActionStepJournalCommand(command="/roll")
    skill = ActionStepSkillCheck(rollModifier="advantage", skillName="Acrobatics")

    assert command.command is Command.Roll
    assert skill.rollModifier is RollModifier.Advantage
    assert skill.skillName == "Acrobatics"


def test_action_step_converts_dict_payloads_and_aliases_for_nested_models():
    attack = ActionStepAttack(
        ability="dex",
        action_type="Bonus Action",
        damage_rolls=[{"abilityName": "dex", "dice": "1d6", "type": "Slashing"}],
        is_proficient=True,
        is_ranged=True,
        long_range=30,
        range_=60,
        rolls_attack=False,
        saving_throw={"abilityName": "dex", "difficultyClass": 12},
    )
    step = ActionStep(
        type="journal-command",
        journalCommand={"command": "/whisper", "args": "secret"},
        skillCheck={"rollModifier": "advantage", "skillName": "Stealth"},
        attack=attack,
    )

    assert step.attack.actionType is ActionType.BonusAction
    assert step.attack.damageRolls[0].dice == Dice("1d6")
    assert step.journalCommand.command is Command.Whisper
    assert step.skillCheck.rollModifier is RollModifier.Advantage


def test_action_step_from_api_normalizes_nested_payloads():
    step = ActionStep.from_api(
        {
            "type": "skill-check",
            "skillCheck": {"rollModifier": "advantage", "skillName": "Perception"},
        }
    )

    assert step.type is ActionStepType.SkillCheck
    assert step.skillCheck.rollModifier is RollModifier.Advantage
    assert step.skillCheck.skillName == "Perception"


def test_action_rejects_invalid_component_and_missing_dice_values():
    with pytest.raises(TypeError):
        Action(steps=["not-a-step"])  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        ActionStepDamage("str", dice={})

    with pytest.raises(TypeError):
        ActionStep(type=ActionStepType.CustomAttack, attack="bad-attack")  # type: ignore[arg-type]


def test_action_step_aliases_and_conflicting_values_cover_branch_paths():
    with pytest.raises(ValueError):
        ActionStepAttack(actionType="Action", action_type="Bonus Action")

    damage = ActionStepDamage(ability_name="wis", type_="Radiant", bonus_or_dice="1d4")
    command = ActionStepJournalCommand(command_name=Command.Me, args="hello")
    skill = ActionStepSkillCheck(roll_modifier="disadvantage", skill_name="Intimidation")

    assert damage.abilityName == "wis"
    assert damage.type == "Radiant"
    assert str(damage.dice) == "1d4"
    assert command.command is Command.Me
    assert skill.rollModifier is RollModifier.Disadvantage
    assert skill.skillName == "Intimidation"


def test_action_step_supports_aliases_for_all_payload_variants_and_serialization():
    step = ActionStep(
        type="custom-attack",
        journal_command={"command": "me", "args": "hello"},
        dice_roll=[ActionStepDamage("str", 1, "1d6")],
        skill_check={"rollModifier": "disadvantage", "skillName": "Arcana"},
        attack={
            "ability": "str",
            "actionType": "Reaction",
            "crit": 19,
            "damageRolls": [{"abilityName": "str", "dice": "1d8", "type": "Force"}],
            "isProficient": False,
            "isRanged": True,
            "name": "Burst",
            "range_": 30,
            "longRange": 60,
            "rollsAttack": True,
            "savingThrow": {"abilityName": "str", "difficultyClass": 14},
        },
    )

    action = Action(
        description="Reaction",
        name="Arcane Burst",
        sort_order=2,
        steps=[step],
    )
    payload = action.to_api()

    assert step.type is ActionStepType.CustomAttack
    assert step.journalCommand.command is Command.Me
    assert step.diceRoll[0].bonus == 1
    assert step.skillCheck.rollModifier is RollModifier.Disadvantage
    assert payload["steps"][0]["journalCommand"]["args"] == "hello"
    assert payload["steps"][0]["attack"]["range"] == 30
    assert payload["steps"][0]["attack"]["longRange"] == 60
    assert payload["sortOrder"] == 2


def test_action_from_api_handles_action_step_objects_and_serializes_all_payload_shapes():
    payload = {
        "description": "Reaction.",
        "name": "Arcane Burst",
        "sortOrder": 1,
        "steps": [
            {
                "type": "custom-attack",
                "journalCommand": {"command": "/whisper", "args": "quiet"},
                "skillCheck": {"rollModifier": "advantage", "skillName": "Perception"},
                "attack": {
                    "ability": "int",
                    "actionType": "Reaction",
                    "crit": 20,
                    "damageRolls": [{"abilityName": "int", "dice": "1d10", "type": "Psychic"}],
                    "isProficient": True,
                    "isRanged": False,
                    "name": "Ping",
                    "rollsAttack": False,
                    "savingThrow": {"abilityName": "int", "difficultyClass": 10},
                },
            }
        ],
    }

    action = Action.from_api(payload)
    assert action.steps[0].attack.actionType is ActionType.Reaction
    assert action.steps[0].journalCommand.command is Command.Whisper
    assert action.steps[0].skillCheck.skillName == "Perception"
    assert action.to_api()["steps"][0]["skillCheck"]["rollModifier"] == "advantage"