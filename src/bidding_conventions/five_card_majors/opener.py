# five_card_majors/opener.py

import random

from bfgdealer.dealer_solo import Dealer
from bridgeobjects import BALANCED_SHAPES, Hand

from bidding_conventions.common import bid_options, hand_shape, suit_html
from bidding_conventions.constants import (
    WHAT_IS_YOUR_BID,
)
from bidding_conventions.descriptions import get_description
from bidding_conventions.question import Question

CONVENTION_TITLE = "5 Card Majors - opening bid"
CONVENTION_DESCRIPTION = get_description("fcm_opening.html")


class Opener:
    @property
    def question(self) -> Question:
        """
        Build the question.
        """
        hand = self._get_hand()
        # hand = Hand("AQ43.KQ654.K3.95")
        correct = self._correct_reponse(hand)
        return Question(
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=self._build_preamble(hand),
            question=WHAT_IS_YOUR_BID,
            options=bid_options("1C", "2NT"),
            correct_response=correct,
        )

    def _get_hand(self) -> Hand:
        dealer = Dealer()
        found = False
        stage = dealer.set_hands_list.index("Opening ones")
        while not found:
            board = dealer.get_set_hand([stage], "N")
            return board.hands["N"]

    def _build_preamble(self, hand: Hand) -> str:
        return f"You hold {hand_shape(hand)} and have {hand.hcp} points"

    def _correct_reponse(self, hand: Hand) -> str:
        if 15 <= hand.hcp <= 17 and hand.shape in BALANCED_SHAPES:
            return "1NT"
        if hand.hearts >= 5 and hand.spades <= hand.hearts:
            return f"1{suit_html('H')}"
        if hand.spades >= 5 and hand.spades > hand.hearts:
            return f"1{suit_html('S')}"
        if hand.diams >= 4 and hand.diams > hand.clubs:
            return f"1{suit_html('D')}"
        return f"1{suit_html('C')}"


def question() -> Question:
    classes = [
        Opener(),
    ]
    return random.choice(classes).question
