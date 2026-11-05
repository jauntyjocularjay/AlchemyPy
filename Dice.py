
import random

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
