from dataclasses import dataclass, field
from enum import StrEnum

from pytilities import ( validate_as )
from .ability_score import AbilityScore
from .dice import Dice
from .saving_throw import SavingThrow


class Command(StrEnum):
    Me = "/me"
    Roll = "/roll"
    Whisper = "/whisper"


class ActionType(StrEnum):
    Action = "Action"
    BonusAction = "Bonus Action"
    Reaction = "Reaction"


class RollModifier(StrEnum):
    Advantage = "advantage"
    Disadvantage = "disadvantage"


class ActionStepType(StrEnum):
    Message = "message"
    JournalCommand = "journal-command"
    CustomDiceRoll = "custom-dice-roll"
    CustomAttack = "custom-attack"
    SkillCheck = "skill-check"


@dataclass(init=False)
class ActionStepAttack:
    ability: AbilityScore | str | None = None
    action_type: ActionType = ActionType.Action
    bonus: int = 0
    crit: int = 20
    damage_rolls: list["ActionStepDamage"] = field(default_factory=list)
    is_proficient: bool = False
    is_ranged: bool = False
    name: str = ""
    range: int | None = None
    long_range: int | None = None
    rolls_attack: bool = True
    saving_throw: SavingThrow | dict = field(default_factory=dict)

    def __init__(
        self,
        ability: AbilityScore | str | None = None,
        action_type: ActionType  | None = None,
        bonus: int = 0,
        crit: int = 20,
        damage_rolls: list[ActionStepDamage] | ActionStepDamage | None = None,
        is_proficient: bool = False,
        is_ranged: bool = False,
        name: str = "",
        range: int | None = None,
        long_range: int | None = None,
        rolls_attack: bool = True,
        saving_throw: SavingThrow | None = None,
    ):
        self.ability = ability
        self.action_type = action_type
        self.bonus = bonus
        self.crit = crit

        if(type(damage_rolls) is list[ActionStepDamage]):
            self.damage_rolls = damage_rolls
        elif(type(damage_rolls) is ActionStepDamage):
            self.damage_rolls = [damage_rolls]
        else:
            self.damage_rolls = None

        self.is_proficient = is_proficient
        self.is_ranged = is_ranged
        self.name = name
        self.range = range if is_ranged else 0
        self.long_range = long_range if is_ranged else 0
        self.rolls_attack = rolls_attack
        self.saving_throw = saving_throw


@dataclass(init=False)
class ActionStepDamage:
    ability_name: str
    bonus: int = 0
    dice: Dice = field(default_factory=lambda: Dice("1d1"))
    type: str = ""

    def __init__(
        self,
        ability_name: str | None = None,
        bonus: int | None = 0,
        dice: Dice | str = '1d6',
        type: str | None = None,
    ):
        validate_as()
        
        self.ability_name = ability_name if ability_name is not None else ''
        self.bonus = bonus if bonus is not None else 0
        self.dice = dice if type(dice) is Dice else Dice(dice)
        self.type = type if type is not None else ''


@dataclass()
class ActionStepJournalCommand:
    command: Command
    args: str = ''


@dataclass()
class ActionStepSkillCheck:
    roll_modifier: RollModifier
    skillName: str = ''


@dataclass()
class ActionStep:
    type: ActionStepType
    journal_command: ActionStepJournalCommand | None = None
    dice_roll: list[ActionStepDamage] | None = None
    attack: ActionStepAttack | None = None
    skill_check: ActionStepSkillCheck | None = None



# LLM-Generated: Completed the Action model and API normalization helpers.

def _serialize_attack(attack: ActionStepAttack | None) -> dict:
    if attack is None:
        return {}

    payload = {
        "ability": attack.ability,
        "actionType": attack.action_type.value if hasattr(attack.action_type, "value") else str(attack.action_type),
        "bonus": attack.bonus,
        "crit": attack.crit,
        "damageRolls": [
            {
                "abilityName": damage.ability_name,
                "bonus": damage.bonus,
                "dice": str(damage.dice),
                "type": damage.type,
            }
            for damage in attack.damage_rolls
        ],
        "isProficient": attack.is_proficient,
        "isRanged": attack.is_ranged,
        "name": attack.name,
        "rollsAttack": attack.rolls_attack,
        "savingThrow": attack.saving_throw,
    }
    if attack.range is not None:
        payload["range"] = attack.range
    if attack.long_range is not None:
        payload["longRange"] = attack.long_range
    return payload


def _serialize_step(step: ActionStep) -> dict:
    payload = {
        "type": step.type.value if hasattr(step.type, "value") else str(step.type),
    }
    if step.attack is not None:
        payload["attack"] = _serialize_attack(step.attack)
    if step.journal_command is not None:
        payload["journalCommand"] = {
            "command": step.journal_command.command.value if hasattr(step.journal_command.command, "value") else str(step.journal_command.command),
            "args": step.journal_command.args,
        }
    if step.skill_check is not None:
        payload["skillCheck"] = {
            "rollModifier": step.skill_check.roll_modifier.value if hasattr(step.skill_check.roll_modifier, "value") else str(step.skill_check.roll_modifier),
            "skillName": step.skill_check.skillName,
        }
    return payload


@dataclass(init=False)
class Action:
    description: str = ""
    name: str = ""
    sortOrder: int = 0
    steps: list[ActionStep] = field(default_factory=list)

    def __init__(
        self,
        description: str = "",
        name: str = "",
        sortOrder: int = 0,
        steps: list[ActionStep | dict] | None = None,
        sort_order: int | None = None,
    ):
        if sort_order is not None:
            sortOrder = sort_order

        if not isinstance(description, str):
            raise TypeError("description must be a string")
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(sortOrder, int):
            raise TypeError("sortOrder must be an integer")

        normalized_steps: list[ActionStep] = []
        if steps is not None:
            if not isinstance(steps, list):
                raise TypeError("steps must be a list or None")
            for item in steps:
                if isinstance(item, ActionStep):
                    normalized_steps.append(item)
                elif isinstance(item, dict):
                    normalized_steps.append(ActionStep.from_api(item))
                else:
                    raise TypeError(f"steps[{item}] must be an ActionStep or dict")

        self.description = description
        self.name = name
        self.sortOrder = sortOrder
        self.steps = normalized_steps

    @classmethod
    def from_api(cls, payload: dict):
        if not isinstance(payload, dict):
            raise TypeError("action payload must be a dict")
        return cls(
            description=str(payload.get("description", "")),
            name=str(payload.get("name", "")),
            sortOrder=int(payload.get("sortOrder", 0)),
            steps=payload.get("steps", []),
        )

    def to_api(self) -> dict:
        return {
            "description": self.description,
            "name": self.name,
            "sortOrder": self.sortOrder,
            "steps": [_serialize_step(step) for step in self.steps],
        }

