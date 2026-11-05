from dataclasses import dataclass


@dataclass
class AbilityScore:
    name: str
    score: int

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("AbilityScore.name must be a non-empty string")
        if not isinstance(self.score, int):
            raise TypeError("AbilityScore.score must be an integer")
