from dataclasses import dataclass, field
from enum import StrEnum

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
    actionType: ActionType = ActionType.Action
    bonus: int = 0
    crit: int = 20
    damageRolls: list["ActionStepDamage"] = field(default_factory=list)
    isProficient: bool = False
    isRanged: bool = False
    name: str = ""
    range: int | None = None
    longRange: int | None = None
    rollsAttack: bool = True
    savingThrow: SavingThrow | dict = field(default_factory=dict)

    def __init__(
        self,
        ability: AbilityScore | str | None = None,
        actionType: ActionType | str | None = None,
        action_type: ActionType | str | None = None,
        bonus: int = 0,
        crit: int = 20,
        damageRolls: list["ActionStepDamage"] | None = None,
        damage_rolls: list["ActionStepDamage"] | None = None,
        isProficient: bool = False,
        is_proficient: bool = False,
        isRanged: bool = False,
        is_ranged: bool = False,
        name: str = "",
        range_: int | None = None,
        longRange: int | None = None,
        long_range: int | None = None,
        rollsAttack: bool = True,
        rolls_attack: bool = True,
        savingThrow: SavingThrow | dict | None = None,
        saving_throw: SavingThrow | dict | None = None,
    ):
        if actionType is not None and action_type is not None and actionType != action_type:
            raise ValueError("actionType and action_type cannot both be provided with different values")
        resolved_action_type = actionType if actionType is not None else action_type
        resolved_damage_rolls = damageRolls if damageRolls is not None else damage_rolls
        resolved_is_proficient = isProficient if isProficient else is_proficient
        resolved_is_ranged = isRanged if isRanged else is_ranged
        resolved_long_range = longRange if longRange is not None else long_range
        resolved_rolls_attack = rollsAttack if rollsAttack else rolls_attack
        resolved_saving_throw = savingThrow if savingThrow is not None else saving_throw

        if resolved_damage_rolls is not None:
            normalized_damage_rolls = []
            for item in resolved_damage_rolls:
                if isinstance(item, ActionStepDamage):
                    normalized_damage_rolls.append(item)
                elif isinstance(item, dict):
                    normalized_damage_rolls.append(ActionStepDamage(**item))
                else:
                    raise TypeError(f"damageRolls[{item}] is not type {ActionStepDamage} or dict")
            resolved_damage_rolls = normalized_damage_rolls

        self.ability = ability
        self.actionType = ActionType(resolved_action_type) if isinstance(resolved_action_type, str) else (resolved_action_type or ActionType.Action)
        self.bonus = bonus
        self.crit = crit
        self.damageRolls = resolved_damage_rolls if resolved_damage_rolls is not None else []
        self.isProficient = resolved_is_proficient
        self.isRanged = resolved_is_ranged
        self.name = name
        self.range = range_
        self.longRange = resolved_long_range
        self.rollsAttack = resolved_rolls_attack
        self.savingThrow = resolved_saving_throw if resolved_saving_throw is not None else {}


@dataclass(init=False)
class ActionStepDamage:
    abilityName: str
    bonus: int = 0
    dice: Dice = field(default_factory=lambda: Dice("1d1"))
    type: str = ""

    def __init__(
        self,
        abilityName: str | None = None,
        bonus_or_dice: int | Dice | str | None = None,
        dice: Dice | str | None = None,
        type: str | None = None,
        ability_name: str | None = None,
        type_: str | None = None,
    ):
        if abilityName is None:
            abilityName = ability_name
        if type is None:
            type = type_

        self.abilityName = abilityName
        self.bonus = 0
        self.type = type if type is not None else ""

        if isinstance(bonus_or_dice, int):
            self.bonus = bonus_or_dice
            resolved_dice = dice
        elif isinstance(bonus_or_dice, (Dice, str)):
            resolved_dice = bonus_or_dice
        else:
            resolved_dice = dice

        if isinstance(resolved_dice, str):
            self.dice = Dice(resolved_dice)
        elif isinstance(resolved_dice, Dice):
            self.dice = resolved_dice
        elif resolved_dice is not None:
            raise TypeError(f"{resolved_dice} is an invalid type for the dice parameter")
        else:
            raise TypeError("dice is required")

        if self.type == "" and isinstance(dice, str):
            self.type = dice


@dataclass(init=False)
class ActionStepJournalCommand:
    command: Command | None = None
    args: str = ""

    def __init__(self, command: Command | str | None = None, args: str = "", command_name: Command | str | None = None):
        if command is None:
            command = command_name
        if isinstance(command, str):
            normalized = command.strip()
            if normalized.lower() in {"/me", "me"}:
                command = Command.Me
            elif normalized.lower() in {"/roll", "roll"}:
                command = Command.Roll
            elif normalized.lower() in {"/whisper", "whisper"}:
                command = Command.Whisper
            else:
                command = Command(normalized)
        self.command = command
        self.args = args


@dataclass(init=False)
class ActionStepSkillCheck:
    rollModifier: RollModifier | None = None
    skillName: str = ""

    def __init__(
        self,
        rollModifier: RollModifier | str | None = None,
        skillName: str = "",
        roll_modifier: RollModifier | str | None = None,
        skill_name: str = "",
    ):
        if rollModifier is None:
            rollModifier = roll_modifier
        if skillName == "":
            skillName = skill_name
        if isinstance(rollModifier, str):
            rollModifier = RollModifier(rollModifier.lower())
        self.rollModifier = rollModifier
        self.skillName = skillName


@dataclass(init=False)
class ActionStep:
    type: ActionStepType | None = None
    journalCommand: ActionStepJournalCommand | None = None
    diceRoll: list[ActionStepDamage] | None = None
    attack: ActionStepAttack | None = None
    skillCheck: ActionStepSkillCheck | None = None

    def __init__(
        self,
        type: ActionStepType | str | None = None,
        journalCommand: ActionStepJournalCommand | dict | None = None,
        journal_command: ActionStepJournalCommand | dict | None = None,
        diceRoll: list[ActionStepDamage] | None = None,
        dice_roll: list[ActionStepDamage] | None = None,
        attack: ActionStepAttack | dict | None = None,
        skillCheck: ActionStepSkillCheck | dict | None = None,
        skill_check: ActionStepSkillCheck | dict | None = None,
    ):
        resolved_journal_command = journalCommand if journalCommand is not None else journal_command
        resolved_dice_roll = diceRoll if diceRoll is not None else dice_roll
        resolved_skill_check = skillCheck if skillCheck is not None else skill_check

        if isinstance(type, str):
            self.type = ActionStepType(type)
        else:
            self.type = type

        if isinstance(resolved_journal_command, dict):
            resolved_journal_command = ActionStepJournalCommand(**resolved_journal_command)
        if isinstance(resolved_skill_check, dict):
            resolved_skill_check = ActionStepSkillCheck(**resolved_skill_check)
        if isinstance(attack, dict):
            attack = ActionStepAttack(**attack)

        if resolved_journal_command is None and resolved_dice_roll is None and attack is None and resolved_skill_check is None:
            raise ValueError("one of journalCommand, diceRoll, attack, or skillCheck must not be None")

        if resolved_journal_command is not None and not isinstance(resolved_journal_command, ActionStepJournalCommand):
            raise TypeError(f"journalCommand must be {ActionStepJournalCommand} or None")

        if resolved_dice_roll is not None:
            if not isinstance(resolved_dice_roll, list):
                raise TypeError(f"diceRoll must be a list of {ActionStepDamage} or None")
            for item in resolved_dice_roll:
                if not isinstance(item, ActionStepDamage):
                    raise TypeError(f"diceRoll[{item}] is not type {ActionStepDamage}")

        if attack is not None and not isinstance(attack, ActionStepAttack):
            raise TypeError(f"attack must be {ActionStepAttack} or None")

        if resolved_skill_check is not None and not isinstance(resolved_skill_check, ActionStepSkillCheck):
            raise TypeError(f"skillCheck must be {ActionStepSkillCheck} or None")

        self.journalCommand = resolved_journal_command
        self.diceRoll = resolved_dice_roll
        self.attack = attack
        self.skillCheck = resolved_skill_check

    @classmethod
    def from_api(cls, data: dict):
        if not isinstance(data, dict):
            raise TypeError("action step payload must be a dict")

        payload = dict(data)
        step_type = payload.get("type")
        kwargs: dict = {"type": step_type}

        if payload.get("attack") not in (None, {}):
            kwargs["attack"] = payload["attack"]
        if payload.get("journalCommand") not in (None, {}):
            kwargs["journalCommand"] = payload["journalCommand"]
        if payload.get("skillCheck") not in (None, {}):
            kwargs["skillCheck"] = payload["skillCheck"]

        return cls(**kwargs)


# LLM-Generated: Completed the Action model and API normalization helpers.

def _serialize_attack(attack: ActionStepAttack | None) -> dict:
    if attack is None:
        return {}

    payload = {
        "ability": attack.ability,
        "actionType": attack.actionType.value if hasattr(attack.actionType, "value") else str(attack.actionType),
        "bonus": attack.bonus,
        "crit": attack.crit,
        "damageRolls": [
            {
                "abilityName": damage.abilityName,
                "bonus": damage.bonus,
                "dice": str(damage.dice),
                "type": damage.type,
            }
            for damage in attack.damageRolls
        ],
        "isProficient": attack.isProficient,
        "isRanged": attack.isRanged,
        "name": attack.name,
        "rollsAttack": attack.rollsAttack,
        "savingThrow": attack.savingThrow,
    }
    if attack.range is not None:
        payload["range"] = attack.range
    if attack.longRange is not None:
        payload["longRange"] = attack.longRange
    return payload


def _serialize_step(step: ActionStep) -> dict:
    payload = {
        "type": step.type.value if hasattr(step.type, "value") else str(step.type),
    }
    if step.attack is not None:
        payload["attack"] = _serialize_attack(step.attack)
    if step.journalCommand is not None:
        payload["journalCommand"] = {
            "command": step.journalCommand.command.value if hasattr(step.journalCommand.command, "value") else str(step.journalCommand.command),
            "args": step.journalCommand.args,
        }
    if step.skillCheck is not None:
        payload["skillCheck"] = {
            "rollModifier": step.skillCheck.rollModifier.value if hasattr(step.skillCheck.rollModifier, "value") else str(step.skillCheck.rollModifier),
            "skillName": step.skillCheck.skillName,
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

