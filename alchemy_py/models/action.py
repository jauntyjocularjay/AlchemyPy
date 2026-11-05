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

    def __init__(self, command: Command | None = None, args: str = "", command_name: Command | None = None):
        if command is None:
            command = command_name
        self.command = command
        self.args = args


@dataclass(init=False)
class ActionStepSkillCheck:
    rollModifier: RollModifier | None = None
    skillName: str = ""

    def __init__(
        self,
        rollModifier: RollModifier | None = None,
        skillName: str = "",
        roll_modifier: RollModifier | None = None,
        skill_name: str = "",
    ):
        if rollModifier is None:
            rollModifier = roll_modifier
        if skillName == "":
            skillName = skill_name
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
        type: ActionStepType | None = None,
        journalCommand: ActionStepJournalCommand | None = None,
        journal_command: ActionStepJournalCommand | None = None,
        diceRoll: list[ActionStepDamage] | None = None,
        dice_roll: list[ActionStepDamage] | None = None,
        attack: ActionStepAttack | None = None,
        skillCheck: ActionStepSkillCheck | None = None,
        skill_check: ActionStepSkillCheck | None = None,
    ):
        resolved_journal_command = journalCommand if journalCommand is not None else journal_command
        resolved_dice_roll = diceRoll if diceRoll is not None else dice_roll
        resolved_skill_check = skillCheck if skillCheck is not None else skill_check

        self.type = type

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
