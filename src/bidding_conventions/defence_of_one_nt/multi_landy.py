# multi_landy.py

import random

from bridgeobjects import Card, Hand

from bidding_conventions.challenge import Challenge
from bidding_conventions.common import get_bid_suppression, suit_html
from bidding_conventions.constants import (
    RANDOM_MAJOR,
    RANDOM_MINOR,
)
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import (
    one_nt_advancers_hand,
    one_nt_overcaller_hand,
)
from bidding_conventions.text import Text

txt = Text()

DEFEND_ONE_NT = 18
CONVENTION_TITLE = "Multi-Landy defence of 1NT"
CONVENTION_DESCRIPTION = get_description("mullti_landy.html")


class Overcaller:
    @property
    def challenge(self) -> Challenge:
        """
        Pick a holding, pick points, adjust for extremes, build the question.
        """
        holding, correct_response = _random_holding()
        points = (9, 15)
        hand = one_nt_overcaller_hand(holding, points)
        correct = self._extreme_points_adjustment(hand.hcp, correct_response)
        return Challenge(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_YOUR_BID,
            correct_response=correct,
            display_elements=["auction", "hand"],
            auction=["1NT", "cursor"],
            hand_cards=hand.sorted_card_names,
            dealer=hand.dealer,
            vulnerability=hand.vulnerability,
        )

    @staticmethod
    def _extreme_points_adjustment(points: int, response: str) -> str:
        if points < 10:
            return "P"
        if points > 15:
            return "X"
        return response

    def _random_points(self) -> int:
        return random.randint(9, 15)


class AdvancersBid:
    def __init__(self) -> None:
        self.strength = None

    @property
    def challenge(self) -> Challenge:
        holding, overcallers_bid = _random_holding()
        points = (10, 14)
        hand = one_nt_advancers_hand(holding, points)
        advancers_bid = self._advancers_bid(overcallers_bid, hand)
        auction = ["1NT", overcallers_bid, "P", "cursor"]
        bid_suppression = get_bid_suppression(auction)
        return Challenge(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_YOUR_BID,
            correct_response=advancers_bid,
            hand_cards=hand.sorted_card_names,
            display_elements=["auction", "hand"],
            vulnerability=hand.vulnerability,
            auction=auction,
            dealer=hand.dealer,
            bid_suppression=bid_suppression,
        )

    def _advancers_bid(self, overcaller_bid: str, hand: Hand) -> str:
        if overcaller_bid == "2C":
            return self._better_major(hand)
        if overcaller_bid == "2D":
            if hand.hcp >= 13 or hand.losers <= 6:
                return "2NT"
            return "2H"
        if overcaller_bid in ["2H", "2S"]:
            return "P"
        if overcaller_bid == "2NT":
            return self._overcaller_bids_two_nt(hand)

    def _overcaller_bids_two_nt(self, hand: Hand) -> str:
        return "3C"

    def _better_major(self, hand: Hand) -> str:
        if hand.hcp >= 13 or hand.losers <= 6:
            if hand.suit_holding["S"] >= 3:
                return "4S"
            if hand.suit_holding["H"] >= 3:
                return "4H"
            return "2NT"
        if hand.suit_holding["S"] > hand.suit_holding["H"]:
            return "2S"
        return "2H"

    def _get_honours(self, suit: str) -> list:
        return [Card(f"{rank}{suit}") for rank in "AKQJ"]


class AdvancerInterpretation:
    OPTIONS = [
        ("2C", f"5/4  in {suit_html('H')} and {suit_html('S')}"),
        ("2D", "6 card suit"),
        ("2H", f"6{suit_html('H')}"),
        ("2S", f"6{suit_html('S')}"),
        ("2NT", f"5/5  in {suit_html('C')} and {suit_html('D')}"),
    ]

    @property
    def challenge(self) -> Challenge:
        global last_response
        while True:
            selection = random.choice(self.OPTIONS)
            if selection[0] == last_response:
                continue
            break
        last_response = selection[0]

        partners_bid = selection[0]
        correct_response = selection[1]
        options = [item[1] for item in self.OPTIONS]
        return Challenge(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_PARTERS_HOLDING,
            options=options,
            correct_response=correct_response,
            display_elements=["auction"],
            auction=["1NT", partners_bid, "P"],
            dealer="E",
        )


def challenge() -> Challenge:
    classes = [
        Overcaller(),
        AdvancersBid(),
        AdvancerInterpretation(),
    ]
    return random.choice(classes).challenge


def _random_holding() -> tuple[str, str]:
    global last_response

    overcallers_holdings: list[tuple[dict[str, int], str]] = [
        ({"H": 5, "S": 4}, "2C"),
        ({"S": 5, "H": 4}, "2C"),
        ({"H": 5, RANDOM_MINOR: 4}, "2H"),
        ({"H": 5, RANDOM_MINOR: 4}, "2H"),
        ({"S": 5, RANDOM_MINOR: 4}, "2S"),
        ({"S": 5, RANDOM_MINOR: 4}, "2S"),
        ({"H": 5, "S": 4}, "P"),
        ({"S": 5, "H": 4}, "P"),
        ({"H": 6, "S": 2}, "2D"),
        ({"S": 6, "H": 2}, "2D"),
        ({"C": 6, RANDOM_MAJOR: 2}, "2D"),
        ({"D": 6, RANDOM_MAJOR: 2}, "2D"),
        ({"C": 5, "D": 5}, "2NT"),
    ]

    while True:
        holding, correct_response = random.choice(overcallers_holdings)
        if correct_response == "P" or correct_response == last_response:
            continue
        random_minor = random.choice(["C", "D"])
        random_major = random.choice(["H", "S"])
        if RANDOM_MINOR in holding:
            holding[random_minor] = holding[RANDOM_MINOR]
            holding.pop(RANDOM_MINOR)
        if RANDOM_MAJOR in holding:
            holding[random_major] = holding[RANDOM_MAJOR]
            holding.pop(RANDOM_MAJOR)
        last_response = correct_response
        return holding, correct_response


last_response = None
