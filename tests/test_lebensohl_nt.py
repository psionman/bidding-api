# test_responders_first_bid.py
#
# Test hands and expected results are derived from Lebensohl-02.xlsx
# (the "After 1NT-(2x)" table), not from the current implementation.
# Two cases are marked xfail where the code diverges from the sheet
# — see the comments on those cases.

import bridgeobjects as bo
import pytest
from bidding_conventions.miscellaneous.lebensohl_first_bid import (
    ResponseToOneNt,
)


def make_bidder(pbn: str, opponents_bid: str) -> ResponseToOneNt:
    """Build a Responder-like object without invoking __init__'s
    random hand-dealing, so we can supply an exact test hand."""
    bidder = ResponseToOneNt.__new__(ResponseToOneNt)
    bidder.hand = bo.Hand(pbn)
    bidder.opponents_bid = opponents_bid
    bidder.auction = None
    bidder.dealer = None
    return bidder


CASES = [
    # --- Very weak: Pass ("Pass: Natural") --------------------------
    pytest.param(
        "874.QJ965.T75.T7",
        "2H",
        "P",
        id="very_weak_pass",
    ),
    # --- Very weak: Bid ("Pass: Natural") --------------------------
    pytest.param(
        "874.QJ965.T75.T7",
        "2D",
        "2H",
        id="very_weak_bid",
    ),
    # --- Competitive, suit ABOVE x: direct 2y ------------------------
    # 7 HCP, 5-card spades (S ranks above H). shape [5,3,3,2].
    pytest.param(
        "AJ953.32.Q32.543",
        "2H",
        "2S",
        id="competitive_suit_above_x",
    ),
    # --- Competitive, suit BELOW x: direct 3y jump -------------------
    # 6 HCP, 5-card diamonds (D ranks below H). shape [5,3,3,2].
    # Sheet: "3y (y lower than x): Competitive" — a DIRECT jump,
    # not a 2NT relay.
    pytest.param(
        "432.32.AQ953.432",
        "2H",
        "3D",
        id="competitive_suit_below_x",
        marks=pytest.mark.xfail(
            reason=(
                "_competitive_bids falls through to '2NT' for "
                "suit-below-x hands; sheet's 'After 1NT-(2x)' table "
                "shows this as a direct 3y jump instead."
            ),
            strict=True,
        ),
    ),
    # --- Invitational: always 2NT, regardless of suit rank -----------
    # 11 HCP, 5-card spades (S ranks above H).
    # Sheet's Table 1 has no direct invitational action; a direct 3y
    # above x is explicitly the Game-force row. Invitational hands
    # must relay via 2NT first (then show themselves on the second
    # round per the "After 2NT-(P)-3C" table).
    pytest.param(
        "AK953.32.Q32.Q32",
        "2H",
        "2NT",
        id="invitational_suit_above_x",
        marks=pytest.mark.xfail(
            reason=(
                "_invitational_bids returns a direct '3S' jump for "
                "suit-above-x hands; sheet shows direct 3y-above-x "
                "as Game force, not Invitational — invitational "
                "hands must go through the 2NT relay."
            ),
            strict=True,
        ),
    ),
    # --- Game force, suit ABOVE x, 5+ cards: direct 3y jump ----------
    # 13 HCP, 6-card spades.
    pytest.param(
        "AKQ953.32.A32.32",
        "2H",
        "3S",
        id="gameforce_suit_above_x",
    ),
    # --- Game force, balanced, has a stopper: relay via 2NT ----------
    # 14 HCP, 4432 shape, AQ3 stopper in hearts (= x).
    pytest.param(
        "KQ32.AQ3.K432.32",
        "2H",
        "2NT",
        id="gameforce_balanced_with_stopper",
    ),
    # --- Game force, balanced, no stopper, no 4cM: direct 3NT --------
    # 14 HCP, 3433 shape, no honour in hearts, no 4+ card major.
    pytest.param(
        "KQ2.432.AK43.Q32",
        "2H",
        "3NT",
        id="gameforce_balanced_no_stopper_no_4cm",
    ),
    # --- Game force, unbalanced, no stopper, has 4cM: cue bid --------
    # 12 HCP, 5422 shape, no honour in hearts, 5-card spade suit.
    pytest.param(
        "AKJ32.32.KJ87.32",
        "2H",
        "3S",
        id="gameforce_unbalanced_no_stopper_has_4cm",
    ),
    # --- Longest suit == x, invitational+ with a trump honour: X ----
    # Ruling: X = negative double when responder's longest suit is
    # x itself, holding invitational-plus points (10+) and a trump
    # honour in x. 12 HCP, 5-card hearts (KQ) matching x.
    pytest.param(
        "A32.KQ854.K32.43",
        "2H",
        "D",
        id="own_suit_matches_x_invitational_plus_double",
    ),
    # --- Longest suit == x, below invitational points: Pass ---------
    # Same shape/honour as above, but only 5 HCP — below the
    # invitational-plus threshold, so Pass rather than double.
    pytest.param(
        "432.KQ854.432.32",
        "2H",
        "P",
        id="own_suit_matches_x_below_invitational_pass",
    ),
    # --- Longest suit == x, exactly 9 HCP: boundary case ------------
    # 9 HCP with a trump honour in x — below the 10+ invitational-
    # plus threshold, so Pass. Current _has_opponent_suit uses
    # `hcp >= 9`, so it would double here instead.
    pytest.param(
        "KJ2.KQ854.432.32",
        "2H",
        "P",
        id="own_suit_matches_x_nine_hcp_boundary",
        marks=pytest.mark.xfail(
            reason=(
                "_has_opponent_suit doubles at hcp >= 9; the "
                "invitational-plus ruling requires 10+, so a 9-HCP "
                "hand should pass instead."
            ),
            strict=True,
        ),
    ),
]


@pytest.mark.parametrize("pbn, opponents_bid, expected", CASES)
def test_responders_first_bid(pbn, opponents_bid, expected):
    bidder = make_bidder(pbn, opponents_bid)
    bidder.auction = ["1NT", opponents_bid, "cursor"]
    assert bidder._responders_first_bid(bidder.hand, opponents_bid) == expected
