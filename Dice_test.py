import pytest
import json
from Dice import Dice


def test_dice_from_string_parses_count_and_sides():
    dice = Dice("4d6")

    assert dice.count == 4
    assert dice.sides == 6


def test_dice_string_representation_uses_count_and_sides():
    dice = Dice("8d20")

    assert str(dice) == "8d20"


def test_dice_roll_returns_one_result_per_die(monkeypatch):
    dice = Dice("3d6")

    values = [2, 4, 6]
    calls = []

    def fake_randint(low, high):
        calls.append((low, high))
        return values[len(calls) - 1]

    monkeypatch.setattr("random.randint", fake_randint)

    result = dice.roll()

    assert result == values
    assert len(result) == dice.count
    assert calls == [(1, 6), (1, 6), (1, 6)]
    assert dice.result == values


def test_dice_roll_keeps_results_within_die_bounds(monkeypatch):
    dice = Dice("2d10")

    def fake_randint(low, high):
        return high

    monkeypatch.setattr("random.randint", fake_randint)

    result = dice.roll()

    assert result == [10, 10]
    assert all(1 <= value <= 10 for value in result)
