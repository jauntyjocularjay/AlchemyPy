import pytest

import AbilityScore

# LLM-Generated: These tests cover the public constructor contract for AbilityScore.


@pytest.mark.parametrize(
    "name, score",
    [
        ("Strength", 15),
        ("Dexterity", 14),
        ("Constitution", 13),
        ("Wisdom", 12),
        ("Intelligence", 10),
        ("Charisma", 8),
    ],
)
def test_ability_score_constructor_assigns_name_and_score(name, score):
    ability = AbilityScore.AbilityScore(name, score)

    assert isinstance(ability, AbilityScore.AbilityScore)
    assert ability.name == name
    assert ability.score == score


@pytest.mark.parametrize("score", [0, -1, 1, 18, 20])
def test_ability_score_accepts_numeric_scores(score):
    ability = AbilityScore.AbilityScore("Test", score)

    assert ability.score == score


