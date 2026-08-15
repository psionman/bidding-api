import pytest
from bridgeobjects import Hand

from bidding_conventions.defence_of_one_nt.asptro import (
    AdvancersBid,
)

advancers_bid = AdvancersBid()


@pytest.mark.parametrize(
    # Overcall has bid two clubs - test advancer
    "hand_str, expected_bid, description",
    [
        ("9876.32.765.T632", "2D", "weak no support"),
        ("98.3276.765.T632", "2H", "weak with support"),
        ("A876.K2.Q65.T632", "2D", "intermediate no support"),
        (
            "AK6.862.Q65.J632",
            "2H",
            "intermediate with 3 card support no honour",
        ),
        (
            "A86.K62.Q65.T632",
            "2H",
            "intermediate with 3 card support with honour ????",
        ),
        ("A86.K642.Q65.J63", "3H", "intermediate with 4 card support"),
        ("AK76.32.AQ5.A632", "2NT", "strong no support"),
        ("32.AK76.AQ5.A632", "4H", "strong with support"),
    ],
)
def test_advancers_bid_two_clubs(hand_str, expected_bid, description):
    hand = Hand(hand_str)
    bid = advancers_bid._advancers_bid("2C", hand)
    assert bid == expected_bid, f"Failed: {description}"


@pytest.mark.parametrize(
    "hand_str, expected_bid, description",
    [
        ("32.79876.65.T632", "2H", "weak no support"),
        ("3276.98.765.T632", "2S", "weak with support"),
        ("K2.A876.Q65.T632", "2H", "intermediate no support"),
        (
            "862.AK6.Q65.J632",
            "2S",
            "intermediate with 3 card support no honour",
        ),
        (
            "K62.A86.Q65.T632",
            "2S",
            "intermediate with 3 card support with honour ????",
        ),
        ("K642.A86.Q65.J63", "3S", "intermediate with 4 card support"),
        ("A32.K76.AQ5.A632", "2NT", "strong no support"),
        ("AK76.32.AQ5.A632", "4S", "strong with support"),
    ],
)
def test_advancers_bid_two_diamonds(hand_str, expected_bid, description):
    hand = Hand(hand_str)
    bid = advancers_bid._advancers_bid("2D", hand)
    assert bid == expected_bid, f"Failed: {description}"


@pytest.mark.parametrize(
    "hand_str, expected_bid, description",
    [
        ("32.9876.765.T632", "P", "< 9  points"),
        ("A2.9876.K65.QJ32", "4H", "10 points, support, 4H"),
        ("A2.K9876.65.QJ32", "4H", "10 pointss, support, 5H"),
        ("A2.K9.KQ765.Q632", "2NT", "13 points, no H"),
    ],
)
def test_advancers_bid_two_hearts(hand_str, expected_bid, description):
    hand = Hand(hand_str)
    bid = advancers_bid._advancers_bid("2H", hand)
    assert bid == expected_bid, f"Failed: {description}"
