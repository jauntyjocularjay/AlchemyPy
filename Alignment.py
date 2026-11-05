from enum import StrEnum

class Morality(StrEnum):
    Good = "Good",
    Neutral = "Neutral",
    Evil = "Evil"

class Order(StrEnum):
    Lawful = "Lawful",
    Neutral = "Neutral",
    Chaotic = "Chaotic"

class Alignment():
    morality: Morality
    order: Order

    def __init__(self, morality: Morality, order: Order):
        self.morality = morality
        self.order = order

    def __str__(self):
        return f'{self.order} {self.morality}'


