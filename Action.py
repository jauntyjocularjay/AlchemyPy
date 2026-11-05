from enum import Enum
import AbilityScore
import SavingThrow
import random

class Command(Enum):
    Me = '/me'
    Roll = '/roll'
    Whisper = '/whisper'

class ActionType(Enum):
    Action = 'Action'
    BonusAction = 'Bonus Action'
    Reaction = 'Reaction'

class RollModifier(Enum):
    Advantage = 'advantage'
    Disadvantage = 'disadvantage'

class ActionStepType(Enum):
    Message = 'message',
    JournalCommand = 'journal-command',
    CustomDiceRoll = 'custom-dice-roll',
    CustomAttack = 'custom-attack',
    SkillCheck = 'skill-check'

class Dice:
    count: int
    sides: int
    result: list[int] = [] # Stores the last result of the roll of Dice

    def __init__(self, count: int, sides: int):
        self.count = count
        self.sides = sides

    def __init__(self, string: str):
        d_index = string.index('d')
        self.count = int(string[:d_index])
        self.sides = int(string[d_index+1:])

    def __str__(self):
        return f'{self.count}d{self.sides}'

    def roll(self):
        self.result = [random.randint(1, self.sides) for i in range(self.count)]
        return self.result


class ActionStepAttack:
    ability: AbilityScore
    actionType: ActionType
    bonus: int
    crit: int
    damageRolls: list[ActionStepDamage] = []
    isProficient: bool
    isRanged: bool
    name: str
    range: int
    longRange: int
    rollsAttack: bool
    savingThrow: SavingThrow


class ActionStepDamage:
    abilityName: str
    bonus: int
    dice: Dice
    type: str

    def __init__(self, abilityName: str, bonus: int, dice: Dice|str, type:str):
        self.abilityName = abilityName,
        self.bonus = bonus
        self.type = type

        if(type(dice) == str):
            self.dice = Dice(str)
        elif(type(dice) == Dice):
            self.dice = dice
        else:
            raise TypeError(f'{dice} is an invalid type for the dice parameter')


class ActionStepJournalCommand:
    command: Command
    args: str

    def __init__(self, command:Command, args: str):
        self.command = command
        self.args = args

class ActionStepSkillCheck:
    rollModifier: RollModifier
    skillName: str

    def __init__(self, rollModifier: RollModifier, skillName: str):
        self.rollModifier = rollModifier
        self.skillName = skillName

class ActionStep:
    type: ActionStepType
    journalCommand: ActionStepJournalCommand|None
    diceRoll: list[ActionStepDamage]|None
    attack: ActionStepAttack|None
    skillCheck: ActionStepSkillCheck|None

    def __init__(self, type: ActionStepType, journalCommand: ActionStepJournalCommand|None = None, diceRoll: ActionStepDamage|None = None, attack: ActionStepAttack|None = None, skillCheck: ActionStepSkillCheck|None = None):
        self.type = type

        if(journalCommand is None and diceRoll is None and attack is None and skillCheck is None):
            raise ValueError(f'one of journalCommand: {journalCommand}, diceRoll: {diceRoll}, attack: {attack}, skillCheck: {skillCheck} must NOT be {None}')
        elif(journalCommand is not None and type(journalCommand) is not ActionStepJournalCommand):
            raise TypeError(f'journalCommand must be {ActionStepJournalCommand} or {None}')
        elif(diceRoll is not None):
            if type(diceRoll) is not list[ActionStepDamage]:
                raise TypeError(f'diceRoll must be a {list} of {ActionStepDamage} or {None}')
            for x in diceRoll:
                if(type(x) is not ActionStepDamage):
                    raise TypeError(f'diceRoll[{x}] is not type {ActionStepDamage}')            
        elif(journalCommand is not None and type(journalCommand) is not ActionStepJournalCommand):
            raise TypeError(f'journalCommand must be {ActionStepJournalCommand} or {None}')
        elif(journalCommand is not None and type(journalCommand) is not ActionStepJournalCommand):
            raise TypeError(f'journalCommand must be {ActionStepJournalCommand} or {None}')

        self.journalCommand = journalCommand if journalCommand is not None else None
        self.diceRoll = diceRoll if diceRoll is not None else None
        self.attack = attack if attack is not None else None
        self.skillCheck = skillCheck if skillCheck is not None else None


class Action:
    description: str
    name: str
    sortOrder: int
    steps: list[ActionStep] = []



