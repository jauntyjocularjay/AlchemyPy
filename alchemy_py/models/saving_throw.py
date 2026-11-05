from dataclasses import dataclass


@dataclass
class SavingThrow:
    abilityName: str
    difficultyClass: int

    def __post_init__(self):
        if not isinstance(self.abilityName, str) or not self.abilityName.strip():
            raise ValueError("abilityName must be a non-empty string")
        if not isinstance(self.difficultyClass, int):
            raise TypeError("difficultyClass must be an integer")
