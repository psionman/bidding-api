# asptro.py

import random

from bfgdealer.dealer_duo import Dealer
from bridgeobjects import Board, Card, Hand

from bidding_conventions.common import hand_strength
from bidding_conventions.constants import (
    OPENER_OPENS_1NT,
    PARTNERS_HOLDING,
    PARTNERS_OVERCALL,
    POINTS,
    RANDOM_MINOR,
    WHAT_IS_YOUR_BID,
    YOUR_HOLDING,
    HandStrength,
)
from bidding_conventions.descriptions import get_description
from bidding_conventions.question import Question, random_minor_suit

DEFEND_ONE_NT = 18
CONVENTION_TITLE = "Asptro defence of 1NT"
CONVENTION_DESCRIPTION = get_description("asptro.html")

IMPLIED_SUIT = {"2C": "H", "2D": "S", "2H": "H", "2S": "S", "2NT": "minors"}


class Overcaller:
    OPTIONS = ["2C", "2D", "2H", "2S", "2NT", "3C", "3D", "X", "P"]
    HOLDINGS = [
        (f"4H and 5{RANDOM_MINOR}", "2C"),
        (f"4S and 5{RANDOM_MINOR}", "2D"),
        (f"5H and 4{RANDOM_MINOR}", "2C"),
        (f"5S and 4{RANDOM_MINOR}", "2D"),
        ("5H and 4S", "2D"),
        ("5S and 4H", "2C"),
        ("5H and 5S", "2D"),
        ("4H and 4S", "P"),
        ("6H", "2H"),
        ("6S", "2S"),
        ("5C and 5D", "2NT"),
    ]

    @staticmethod
    def _extreme_points_adjustment(points: int, response: str) -> str:
        if points < 10:
            return "P"
        if points > 15:
            return "X"
        return response

    def _random_holding(self) -> tuple[str, str]:
        holding, correct_response = random.choice(self.HOLDINGS)
        minor = random_minor_suit(holding)
        return minor, correct_response

    def _random_points(self) -> int:
        return random.randint(9, 15)

    def _build_preamble(self, holding: str, points: int) -> str:
        return (
            f"{OPENER_OPENS_1NT} and {YOUR_HOLDING} "
            f"{holding} and have {points} {POINTS}."
        )

    @property
    def question(self) -> Question:
        """
        Pick a holding, pick points, adjust for extremes, build the question.
        """
        holding, correct_response = self._random_holding()
        points = self._random_points()
        correct = self._extreme_points_adjustment(points, correct_response)
        return Question(
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=self._build_preamble(holding, points),
            question=WHAT_IS_YOUR_BID,
            options=[],
            correct_response=correct,
        )


class AdvancerInterpretation:
    OPTIONS = [
        ("2C", "5/4 H and another"),
        ("2D", "5/4 S and another"),
        ("2H", "6H"),
        ("2S", "6S"),
        ("2NT", "5C and 5D"),
    ]

    @property
    def question(self) -> Question:
        selection = random.choice(self.OPTIONS)
        partners_bid = selection[0]
        correct_response = selection[1]
        preamble = f"{OPENER_OPENS_1NT} {PARTNERS_OVERCALL} {partners_bid}"
        options = [item[1] for item in self.OPTIONS]
        return Question(
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=preamble,
            question=PARTNERS_HOLDING,
            options=options,
            correct_response=correct_response,
        )


class AdvancersBid:
    def __init__(self) -> None:
        self.strength = None

    @property
    def question(self) -> Question:
        board, overcaller_bid = self._get_board()
        advancers_hand = board.hands["W"]
        advancers_bid = self._advancers_bid(overcaller_bid, advancers_hand)

        suit = IMPLIED_SUIT[overcaller_bid]
        if suit == "minors":
            cards = f"{advancers_hand.clubs}C and {advancers_hand.diamonds}D"
        else:
            cards = f"{len(advancers_hand.cards_by_suit[suit])}{suit}"

        preamble = (
            f"{OPENER_OPENS_1NT} {PARTNERS_OVERCALL} {overcaller_bid}"
            f" and {YOUR_HOLDING} {cards} and {advancers_hand.hcp} {POINTS}."
        )
        return Question(
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=preamble,
            question=WHAT_IS_YOUR_BID,
            options=[],
            correct_response=advancers_bid,
        )

    def _get_board(self) -> Board:
        found = False
        while not found:
            board = Dealer().get_set_hand(DEFEND_ONE_NT, "N")
            overcall_hand = board.hands["E"]
            overcaller_bid = self._overcaller_bid(overcall_hand)
            if overcaller_bid:
                found = True

        self.strength = hand_strength(overcall_hand)
        return board, overcaller_bid

    def _overcaller_bid(self, hand: Hand) -> str:
        if self.strength == HandStrength.WEAK:
            return False

        shape = hand.shape
        if shape[0] == 4:
            return None

        if hand.spades >= 6:
            return "2S"
        if hand.hearts >= 6:
            return "2H"
        if hand.spades == 5 and shape[1] >= 4:
            return "2D"
        if hand.hearts == 5 and shape[1] >= 4:
            return "2C"
        if hand.diamonds >= 5 and hand.clubs >= 5:
            return "2NT"

        return None

    def _advancers_bid(self, overcaller_bid: str, hand: Hand) -> str:
        if overcaller_bid == "2C":
            return self._overcaller_bids_minor(hand, "H", "2D")
        if overcaller_bid == "2D":
            return self._overcaller_bids_minor(hand, "S", "2H")
        if overcaller_bid in ["2H", "2S"]:
            return self._overcaller_bids_major(hand, overcaller_bid)

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

    def _get_honours(self, suit: str) -> list:
        return [Card(f"{rank}{suit}") for rank in "AKQJ"]

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

    def _get_card_count(self) -> str:
        card_count = random.randint(0, 5)
        if card_count:
            return str(card_count)
        return "no "


def asptro_question() -> Question:
    classes = [
        Overcaller(),
        AdvancerInterpretation(),
        AdvancersBid(),
    ]
    return random.choice(classes).question
