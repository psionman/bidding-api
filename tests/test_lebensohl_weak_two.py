# test_responders_first_bid_weak_two_doubled.py
#
# Tests for the (2x)-X-(P) auction: opponent opens a weak two,
# partner doubles (takeout), RHO passes, responder to bid.
#
# Lebensohl-02.xlsx headers this table "After 1NT-(2x), or
# (2x)-X-(P)" — it's the SAME base table as the 1NT-overcall
# variant, not a separate convention. What differs is that partner's
# double is forcing: `Responder.is_forcing` becomes True whenever
# auction[1] == "D" and auction[2] == "P", and three branches in the
# shared Responder methods check it:
#
#   1. The "very weak, no fit" top-level guard is skipped entirely
#      when forcing — responder must find *some* action.
#   2. _has_opponent_suit never doubles when forcing (no redouble
#      is modelled) — it always passes.
#   3. _competitive_bids' weak-long-suit branch relays via 2NT
#      instead of passing, when forcing and the barrier isn't
#      broken.
#
# The two known bugs from the 1NT-overcall suite (_competitive_bids
# falling through to 2NT instead of a direct 3y jump when the suit
# ranks below x; _invitational_bids jumping to 3y directly instead
# of relaying via 2NT when the suit ranks above x) live in the same
# shared methods, so they reproduce here too — marked xfail again.

import bridgeobjects as bo
import pytest
from bidding_conventions.miscellaneous.lebensohl_first_bid import (
    ResponseToWeakTwoDoubled,
)


def make_bidder(pbn: str, opponents_bid: str) -> ResponseToWeakTwoDoubled:
    """Build a Responder-like object in the (2x)-X-(P) auction,
    without invoking __init__'s random hand-dealing."""
    bidder = ResponseToWeakTwoDoubled.__new__(ResponseToWeakTwoDoubled)
    bidder.hand = bo.Hand(pbn)
    bidder.opponents_bid = opponents_bid
    bidder.auction = [opponents_bid, "D", "P", "cursor"]
    bidder.dealer = None
    return bidder


CASES = [
    # === is_forcing-specific behaviour ===============================
    # --- Weak, no fit (shape<=4), barrier BROKEN --------------------
    # Opposite a 1NT overcall this hand would just Pass (top-level
    # guard). Here the double is forcing, so the guard is skipped
    # and responder falls through to a natural 2y bid instead.
    # 5 HCP, 4-card spades (unique longest, ranks above H).
    pytest.param(
        "K432.432.432.Q32",
        "2H",
        "2S",
        id="forcing_weak_no_fit_barrier_broken",
    ),
    # --- Weak, no fit (shape<=4), barrier NOT broken -----------------
    # Same idea, but the only 4-card suit ranks below x, so the
    # fallback in _competitive_bids is the 2NT relay.
    # 5 HCP, 4-card clubs (unique longest, ranks below H).
    pytest.param(
        "432.432.Q32.K432",
        "2H",
        "2NT",
        id="forcing_weak_no_fit_barrier_not_broken",
    ),
    # --- Weak, LONG suit (shape>=5), barrier NOT broken --------------
    # Opposite a 1NT overcall this passes (the inner `if not
    # is_forcing: return "P"` branch). Forcing here, so it relays
    # via 2NT instead. 2 HCP, 5-card diamonds, ranks below H.
    pytest.param(
        "432.32.Q9853.432",
        "2H",
        "2NT",
        id="forcing_weak_long_suit_barrier_not_broken",
    ),
    # --- Own suit matches x, high HCP: forced to Pass, not Double ----
    # Opposite a 1NT overcall, 12 HCP with a trump honour in x would
    # double (per the invitational-plus ruling). Here _has_opponent_suit
    # never doubles while forcing — partner already doubled, and
    # redouble isn't modelled — so it passes regardless of strength.
    pytest.param(
        "A32.KQ854.K32.43",
        "2H",
        "P",
        id="forcing_own_suit_matches_x_always_pass",
    ),
    # === Baseline rows, unaffected by is_forcing (sanity checks) =====
    # --- Competitive, suit ABOVE x: direct 2y ------------------------
    pytest.param(
        "AJ953.32.Q32.543",
        "2H",
        "2S",
        id="competitive_suit_above_x",
    ),
    # --- Competitive, suit BELOW x: direct 3y jump -------------------
    # Same shared-method bug as the 1NT-overcall suite: falls
    # through to "2NT" instead of the sheet's direct 3y jump.
    pytest.param(
        "432.32.AQ953.432",
        "2H",
        "3D",
        id="competitive_suit_below_x",
        marks=pytest.mark.xfail(
            reason=(
                "_competitive_bids falls through to '2NT' for "
                "suit-below-x hands regardless of is_forcing; sheet "
                "shows this as a direct 3y jump."
            ),
            strict=True,
        ),
    ),
    # --- Invitational, suit ABOVE x: relay via 2NT --------------------
    # Same shared-method bug: _invitational_bids has no is_forcing
    # check, so it still jumps to a direct 3y (the sheet's
    # Game-force row) instead of relaying.
    pytest.param(
        "AK953.32.Q32.Q32",
        "2H",
        "2NT",
        id="invitational_suit_above_x",
        marks=pytest.mark.xfail(
            reason=(
                "_invitational_bids returns a direct '3S' jump for "
                "suit-above-x hands; sheet reserves direct 3y-above-x "
                "for Game force — invitational hands must relay."
            ),
            strict=True,
        ),
    ),
    # --- Game force, suit ABOVE x, 5+ cards: direct 3y jump ----------
    pytest.param(
        "AKQ953.32.A32.32",
        "2H",
        "3S",
        id="gameforce_suit_above_x",
    ),
    # --- Game force, balanced, has a stopper: relay via 2NT ----------
    pytest.param(
        "KQ32.AQ3.K432.32",
        "2H",
        "2NT",
        id="gameforce_balanced_with_stopper",
    ),
    # --- Game force, balanced, no stopper, no 4cM: direct 3NT --------
    pytest.param(
        "KQ2.432.AK43.Q32",
        "2H",
        "3NT",
        id="gameforce_balanced_no_stopper_no_4cm",
    ),
    # --- Game force, longest suit BELOW x, no stopper, has 4cM: cue -
    # Longest suit (diamonds) doesn't break the barrier, so the
    # natural-jump branch is skipped and the cue bid (denies stop,
    # promises 4cM via the 4-card spade suit) applies.
    pytest.param(
        "KQ32.32.AKJ87.32",
        "2H",
        "3H",
        id="gameforce_unbalanced_no_stopper_has_4cm",
    ),
]


@pytest.mark.parametrize("pbn, opponents_bid, expected", CASES)
def test_responders_first_bid_weak_two_doubled(pbn, opponents_bid, expected):
    bidder = make_bidder(pbn, opponents_bid)
    assert bidder.is_forcing is True
    assert bidder._responders_first_bid(bidder.hand, opponents_bid) == expected
