import pytest

from alchemy_py.models.action import ActionStep, ActionStepAttack, ActionStepDamage, ActionStepType
from alchemy_py.models.alignment import Alignment, Morality, Order
from alchemy_py.models.character import Character
from alchemy_py.models.dice import Dice


def test_package_models_expose_expected_api():
    dice = Dice("4d6")
    assert str(dice) == "4d6"

    alignment = Alignment(Morality.Good, Order.Lawful)
    assert str(alignment) == "Lawful Good"

    damage = ActionStepDamage("str", "1d8", "Slashing")
    attack = ActionStepAttack(
        ability="str",
        actionType="Action",
        damageRolls=[damage],
        name="Slash",
    )
    step = ActionStep(type=ActionStepType.CustomAttack, attack=attack)

    assert attack.damageRolls[0].abilityName == "str"
    assert step.attack is attack


def test_alignment_is_a_frozen_dataclass_value_object():
    alignment = Alignment(Morality.Good, Order.Chaotic)

    assert alignment == Alignment(Morality.Good, Order.Chaotic)
    with pytest.raises(Exception):
        alignment.morality = Morality.Evil


def test_character_defaults_are_safe_and_dataclass_based():
    character = Character()

    assert character.abilityScores == []
    assert character.currentHP == 0
    assert character.maxHP == 0
    assert character.isNPC is False
