import random
from dataclasses import dataclass, field


@dataclass(init=False)
class Dice:
    """A dice expression using the API's canonical `countdside` representation."""

    count: int
    sides: int
    result: list[int] = field(default_factory=list)

    def __init__(self, count_or_string, sides=None):
        if isinstance(count_or_string, str):
            if "d" not in count_or_string:
                raise ValueError(f"Dice strings must use the format 'countdside': {count_or_string!r}")
            d_index = count_or_string.index("d")
            count = int(count_or_string[:d_index])
            sides = int(count_or_string[d_index + 1 :])
        elif isinstance(count_or_string, int) and isinstance(sides, int):
            count = count_or_string
        else:
            raise TypeError("Dice requires either a string like '4d6' or an int count plus a sides value")

        if count <= 0:
            raise ValueError("Dice count must be greater than zero")
        if sides <= 0:
            raise ValueError("Dice sides must be greater than zero")

        self.count = count
        self.sides = sides
        self.result = []

    def __str__(self):
        return f"{self.count}d{self.sides}"

    def roll(self):
        self.result = [random.randint(1, self.sides) for _ in range(self.count)]
        return self.result
