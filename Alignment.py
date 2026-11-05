from enum import Enum

class Morality(Enum):
    Good = "Good",
    Neutral = "Neutral",
    Evil = "Evil"

class Order(Enum):
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


