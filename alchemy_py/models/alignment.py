from dataclasses import dataclass
from enum import StrEnum


class Morality(StrEnum):
    Good = "Good"
    Neutral = "Neutral"
    Evil = "Evil"


class Order(StrEnum):
    Lawful = "Lawful"
    Neutral = "Neutral"
    Chaotic = "Chaotic"


@dataclass(frozen=True)
class Alignment:
    morality: Morality
    order: Order

    def __post_init__(self):
        if not isinstance(self.morality, Morality):
            raise TypeError("morality must be a Morality member")
        if not isinstance(self.order, Order):
            raise TypeError("order must be an Order member")

    def __str__(self):
        return f"{self.order} {self.morality}"
