from enum import Enum
import AbilityScore

from Constants import (
    CURRENT,
    MAX
)
from Alignment import (
    Order,
    Morality,
    Alignment
)

class Color(Enum):
    Blue = 'Blue',
    Green = 'Green', 
    Orange = 'Orange', 
    Purple = 'Purple', 
    Red = 'Red',
    Yellow = 'Yellow'

class TrackerType(Enum):
    Bar = "Bar"
    Pip = "Pip"

class Tracker:
    name: str
    color: Color
    max: int
    type: TrackerType
    value: int

class Character:
    AbilityScores: AbilityScore = []
    alignment: Alignment
    HP = {
        "current": int,
        "maximum": int
    }
    maxHP = HP[MAX]
    currentHP = HP[CURRENT]
    currentHP: int
    exp: int
    initiativeBonus: int
    imageURL: str
    isNPC: bool
    isSpellcaster: bool
    speed: int