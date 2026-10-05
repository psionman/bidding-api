# asptro.py

import random

from bridgeobjects import Card, Hand

from bidding_conventions.challenge import Challenge, random_minor_suit
from bidding_conventions.common import hand_strength, suit_html
from bidding_conventions.constants import (
    HandStrength,
)
from bidding_conventions.convention import NextQuestion
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import (
    one_nt_advancers_hand,
    one_nt_overcaller_hand,
)
from bidding_conventions.text import Text

txt = Text()

CONVENTION_THEME = "Defence of 1NT"
CONVENTION_TITLE = "Asptro"
CONVENTION_DESCRIPTION = get_description("asptro.html")

OVERCALLERS_HOLDINGS = [
    ({"H": 4, "C": 5}, "2C"),
    ({"H": 4, "D": 5}, "2C"),
    ({"S": 4, "C": 5}, "2D"),
    ({"S": 4, "D": 5}, "2D"),
    ({"H": 5, "C": 4}, "2C"),
    ({"H": 5, "D": 4}, "2C"),
    ({"S": 5, "C": 4}, "2D"),
    ({"S": 5, "D": 4}, "2D"),
    ({"H": 5, "S": 4}, "2C"),
    ({"S": 5, "H": 4}, "2D"),
    ({"S": 5, "H": 5}, "2D"),
    ({"S": 4, "H": 4}, "P"),
    ({"H": 6, "S": 2}, "2H"),
    ({"S": 6, "H": 2}, "2S"),
    ({"C": 5, "D": 5}, "2NT"),
]
DEFEND_ONE_NT = 18


class Overcaller:
    @property
    def challenge(self) -> Challenge:
        """
        Pick a holding, pick points, adjust for extremes, build the question.
        """
        holding, correct_response = random_holding()
        points = (9, 15)
        hand = one_nt_overcaller_hand(holding, points)
        correct = self._extreme_points_adjustment(hand.hcp, correct_response)
        return Challenge(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_YOUR_BID,
            correct_response=correct,
            display_elements=["auction", "hand", "bidding_box"],
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
        holding, overcallers_bid = random_holding()
        points = (9, 15)
        hand = one_nt_advancers_hand(holding, points)
        advancers_bid = self._advancers_bid(overcallers_bid, hand)

        question = (txt.WHAT_IS_YOUR_BID,)
        return Challenge(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=question,
            correct_response=advancers_bid,
            hand_cards=hand.sorted_card_names,
            display_elements=["auction", "hand"],
            vulnerability=hand.vulnerability,
            auction=["1NT", overcallers_bid, "P", "cursor"],
            dealer=hand.dealer,
        )

    def _advancers_bid(self, overcaller_bid: str, hand: Hand) -> str:
        if overcaller_bid == "2C":
            return self._overcaller_bids_minor(hand, "H", "2D")
        if overcaller_bid == "2D":
            return self._overcaller_bids_minor(hand, "S", "2H")
        if overcaller_bid in ["2H", "2S"]:
            return self._overcaller_bids_major(hand, overcaller_bid)
        if overcaller_bid == "2NT":
            return self._overcaller_bids_two_nt(hand)

    def _overcaller_bids_minor(
        self,
        hand: Hand,
        suit: str,
        next_suit: str,
    ) -> str:
        self.strength = hand_strength(hand)
        suit_holding = hand.suit_holding[suit]
        honours = self._get_honours(suit)
        if (
            suit_holding >= 3
            and self.strength == HandStrength.WEAK
            and any(map(lambda v: v in honours, hand.cards))
        ):
            return f"2{suit}"
        if suit_holding >= 4 and self.strength == HandStrength.WEAK:
            return f"2{suit}"
        if self.strength == HandStrength.INTERMEDIATE and suit_holding == 3:
            return f"2{suit}"
        if self.strength == HandStrength.INTERMEDIATE and suit_holding >= 4:
            return f"3{suit}"
        if self.strength == HandStrength.STRONG and suit_holding >= 4:
            return f"4{suit}"
        if self.strength == HandStrength.STRONG:
            return "2NT"
        return next_suit

    def _overcaller_bids_major(
        self,
        hand: Hand,
        bid: str,
    ) -> str:
        self.strength = hand_strength(hand)
        suit = bid[1]
        suit_holding = hand.suit_holding[suit]
        if self.strength == HandStrength.INTERMEDIATE and suit_holding >= 4:
            return f"4{suit}"
        if self.strength == HandStrength.STRONG:
            return "2NT"
        return "P"

    def _overcaller_bids_two_nt(self, hand: Hand) -> str:
        self.strength = hand_strength(hand)
        if self.strength == HandStrength.WEAK:
            return "3C"
        if self.strength == HandStrength.INTERMEDIATE:
            return "3C"
        if self.strength == HandStrength.STRONG:
            return "4NT"
        return "P"

    def _get_honours(self, suit: str) -> list:
        return [Card(f"{rank}{suit}") for rank in "AKQJ"]


class AdvancerInterpretation:
    OPTIONS = [
        ("2C", f"5/4 {suit_html('H')} and another"),
        ("2D", f"5/4 {suit_html('S')} and another"),
        ("2H", f"6{suit_html('H')}"),
        ("2S", f"6{suit_html('S')}"),
        ("2NT", f"5{suit_html('C')} and 5{suit_html('D')}"),
    ]

    @property
    def challenge(self) -> Challenge:
        selection = random.choice(self.OPTIONS)
        partners_bid = selection[0]
        correct_response = selection[1]
        question = txt.WHAT_IS_PARTERS_HOLDING
        options = [item[1] for item in self.OPTIONS]
        return Challenge(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=question,
            options=options,
            correct_response=correct_response,
            display_elements=["auction"],
            auction=["1NT", partners_bid, "P"],
            dealer="E",
        )


def random_holding() -> tuple[str, str]:
    holding, correct_response = random.choice(OVERCALLERS_HOLDINGS)
    minor_holding = random_minor_suit(holding)
    return minor_holding, correct_response


QUESTION_CLASSES: list[tuple[type, int]] = [
    (Overcaller, 1),
    (AdvancersBid, 1),
    (AdvancerInterpretation, 1),
]


challenge = NextQuestion(QUESTION_CLASSES).challenge
