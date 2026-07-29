# five_card_majors/opener.py

import random

from bfgdealer.dealer_solo import Dealer
from bridgeobjects import BALANCED_SHAPES, Hand

from bidding_conventions.common import hand_shape
from bidding_conventions.constants import (
    WHAT_IS_YOUR_BID,
)
from bidding_conventions.descriptions import get_description
from bidding_conventions.question import Question

CONVENTION_THEME = "5 Card Majors"
CONVENTION_TITLE = "opening bid"
CONVENTION_DESCRIPTION = get_description("fcm_opening.html")

SUIT_ORDER = ["S", "H", "C", "D"]


class Opener:
    @property
    def question(self) -> Question:
        """
        Build the question.
        """
        hand = self._get_hand()
        # hand = Hand("AQ43.KQ654.K3.95")
        correct = self._correct_reponse(hand).upper()
        return Question(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=self._build_preamble(hand),
            question=WHAT_IS_YOUR_BID,
            options=None,
            correct_response=correct,
            hand_cards=self._sort_hand_cards(hand),
        )

    def _sort_hand_cards(self, hand: Hand) -> list[str]:
        sorted_hand = Hand.sort_card_list(hand.cards, SUIT_ORDER)
        hand_cards = [card.name for card in sorted_hand]
        return hand_cards

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
            return "1H"
        if hand.spades >= 5 and hand.spades > hand.hearts:
            return "1S"
        if hand.diams >= 4 and hand.diams > hand.clubs:
            return "1D"
        return "1C"


def question() -> Question:
    classes = [
        Opener(),
    ]
    return random.choice(classes).question
