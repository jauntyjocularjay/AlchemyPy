from dataclasses import dataclass, field
from enum import Enum

from .ability_score import AbilityScore
from .alignment import Alignment


class Color(Enum):
    Blue = "Blue"
    Green = "Green"
    Orange = "Orange"
    Purple = "Purple"
    Red = "Red"
    Yellow = "Yellow"


class TrackerType(Enum):
    Bar = "Bar"
    Pip = "Pip"


@dataclass
class Tracker:
    name: str
    color: Color
    max: int
    type: TrackerType
    value: int


@dataclass
class Character:
    name: str = ""
    abilityScores: list[AbilityScore] = field(default_factory=list)
    alignment: Alignment | None = None
    currentHP: int = 0
    maxHP: int = 0
    exp: int = 0
    initiativeBonus: int = 0
    imageURL: str | None = None
    isNPC: bool = False
    isSpellcaster: bool = False
    speed: int = 0
    type: str = ""
