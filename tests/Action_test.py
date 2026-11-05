import pytest

from Action import (
    ActionStep,
    ActionStepAttack,
    ActionStepDamage,
    ActionStepType,
    ActionType,
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