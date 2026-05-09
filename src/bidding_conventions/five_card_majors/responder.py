# five_card_majors/responder.py

import random

from bfgdealer.dealer_solo import Dealer
from bridgeobjects import BALANCED_SHAPES, Board, Hand

from bidding_conventions.common import bid_options
from bidding_conventions.constants import (
    WHAT_IS_YOUR_BID,
)
from bidding_conventions.descriptions import get_description
from bidding_conventions.question import Question

CONVENTION_TITLE = "5 Card Majors - opening bid"
CONVENTION_DESCRIPTION = get_description("fcm_opening.html")


class ResponsesToOneClub:
    @property
    def question(self) -> Question:
        """
        Pick a holding, pick points, build the question.
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
        stage = dealer.set_hands_list.index("Opening ones")
        while True:
            board = dealer.get_set_hand([stage], "N")
            hand = board.hands["N"]
            if 15 <= hand.hcp <= 17 and hand.shape in BALANCED_SHAPES:
                continue
            if hand.hearts >= 5 and hand.spades <= hand.hearts:
                continue
            if hand.spades >= 5 and hand.spades > hand.hearts:
                continue
            if hand.diams >= 4 and hand.diams > hand.clubs:
                continue
            print(hand)
            return board.hands["S"]

    def _build_preamble(self, hand: Hand) -> str:
        spades = f"{hand.spades}S, " if hand.spades else ""
        hearts = f"{hand.hearts}H, " if hand.hearts else ""
        diams = f"{hand.diams}D, " if hand.diams else ""
        clubs = f"{hand.clubs}C" if hand.clubs else ""
        shape = f"{spades}{hearts}{diams}{clubs}"
        return (
            f"Partner has opened 1C and you hold {shape} "
            f"and have {hand.hcp} points"
        )

    def _correct_reponse(self, hand: Hand) -> str:
        if 15 <= hand.hcp <= 17 and hand.shape in BALANCED_SHAPES:
            print("1NT")
            return "1NT"
        if hand.hearts >= 5 and hand.spades <= hand.hearts:
            print("1H")
            return "1H"
        if hand.spades >= 5 and hand.spades > hand.hearts:
            print("1S")
            return "1S"
        if hand.diams >= 4 and hand.diams > hand.clubs:
            print("1D")
            return "1D"
        print("1C")
        return "1C"


def question() -> Question:
    classes = [
        ResponsesToOneClub(),
    ]
    return random.choice(classes).question
