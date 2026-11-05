import pytest

from Alignment import Alignment, Morality, Order

# LLM-Generated: Behavior-focused tests for the Alignment enum values and constructor contract.


@pytest.mark.parametrize(
    "member, expected_name",
    [
        (Morality.Good, "Good"),
        (Morality.Neutral, "Neutral"),
        (Morality.Evil, "Evil"),
        (Order.Lawful, "Lawful"),
        (Order.Neutral, "Neutral"),
        (Order.Chaotic, "Chaotic"),
    ],
)
def test_alignment_enums_expose_expected_values(member, expected_name):
    assert member.value == expected_name
    assert member.name == expected_name


@pytest.mark.parametrize(
    "morality, order",
    [
        (Morality.Good, Order.Lawful),
        (Morality.Good, Order.Neutral),
        (Morality.Good, Order.Chaotic),
        (Morality.Neutral, Order.Lawful),
        (Morality.Neutral, Order.Neutral),
        (Morality.Neutral, Order.Chaotic),
        (Morality.Evil, Order.Lawful),
        (Morality.Evil, Order.Neutral),
        (Morality.Evil, Order.Chaotic),
    ],
)
def test_alignment_constructor_assigns_values(morality, order):
    alignment = Alignment(morality, order)

    assert alignment.morality is morality
    assert alignment.order is order


@pytest.mark.parametrize(
    "morality, order, expected",
    [
        (Morality.Good, Order.Lawful, "Lawful Good"),
        (Morality.Neutral, Order.Neutral, "Neutral Neutral"),
        (Morality.Evil, Order.Chaotic, "Chaotic Evil"),
    ],
)
def test_alignment_string_representation_uses_order_then_morality(morality, order, expected):
    alignment = Alignment(morality, order)

    assert str(alignment) == expected
