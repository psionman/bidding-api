# five_card_majors/responder.py

import random

from bfgdealer.dealer_solo import Dealer
from bridgeobjects import BALANCED_SHAPES, Hand

from bidding_conventions.common import hand_shape
from bidding_conventions.descriptions import get_description
from bidding_conventions.question import Question
from bidding_conventions.text import Text

txt = Text()

CONVENTION_THEME = "5 Card Majors"
CONVENTION_TITLE = "Responder"
CONVENTION_DESCRIPTION = get_description("fcm_opening.html")


class ResponsesToOneClub:
    @property
    def question(self) -> Question:
        """Build the question."""
        hand = self._get_hand()
        hand = Hand("AQ43.KQ54.K93.95")
        # hand = Hand("AQ43.KQ65.843.95")
        return Question(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=self._build_preamble(hand),
            question=txt.WHAT_IS_YOUR_BID,
            options=None,
            correct_response=self._correct_reponse(hand).upper(),
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
            return board.hands["S"]

    def _build_preamble(self, hand: Hand) -> str:
        return (
            f"Partner has opened 1C and you hold {hand_shape(hand)} "
            f"and have {hand.hcp} points"
        )

    def _correct_reponse(self, hand: Hand) -> str:
        if hand.hcp < 5:
            return "P"

        if hand.hcp >= 12 and hand.hearts >= 4 and hand.spades <= hand.hearts:
            return "1H"
        if hand.hcp <= 12 and hand.spades >= 4:
            return "1S"
        if hand.hcp <= 12 and hand.diams >= 5:
            return "1D"

        # Walsh responses
        if hand.hcp <= 11 and hand.hearts >= 4 and hand.spades <= hand.hearts:
            return "1H"
        if hand.hcp <= 11 and hand.spades >= 4:
            return "1S"

        #  Inverted minors (strong)
        if hand.clubs >= 6 or hand.clubs == 5 and hand.suit_points("C") >= 7:
            return "2C"

        # weak jump responses
        if hand.hcp <= 9 and hand.diams >= 6:
            return "2D"
        if hand.hcp <= 9 and hand.hearts >= 6:
            return "2H"
        if hand.hcp <= 9 and hand.spades >= 6:
            return "2S"

        # Balanced invitational
        if hand.is_balanced and 11 <= hand.hcp <= 12:
            return "2NT"

        # preemptive responses
        if hand.hcp <= 9 and hand.clubs >= 6:
            return "3C"
        if hand.hcp <= 9 and hand.diams >= 7:
            return "3D"
        if hand.hcp <= 9 and hand.hearts >= 7:
            return "3H"
        if hand.hcp <= 9 and hand.spades >= 7:
            return "3S"

        # NT game sign-off
        # TODO come back to this if slam invitational
        if (
            hand.is_balanced
            and 13 <= hand.hcp <= 15
            and self.hearts <= 4
            and self.spades <= 4
        ):
            return "3NT"
        return "1NT"


class ResponsesToOneNoTrumps:
    @property
    def question(self) -> Question:
        """Build the question."""
        hand = self._get_hand()
        return Question(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=self._build_preamble(hand),
            question=txt.WHAT_IS_YOUR_BID,
            options=None,
            correct_response=self._correct_reponse(hand).upper(),
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
            return board.hands["S"]

    def _build_preamble(self, hand: Hand) -> str:
        return (
            f"Partner has opened 1NT and you hold {hand_shape(hand)} "
            f"and have {hand.hcp} points"
        )

    def _correct_reponse(self, hand: Hand) -> str:
        if hand.hcp <= 9 and not hand.five_card_major_or_better:
            return "P"

        # Slam try
        if hand.hcp + hand.shape[0] + hand.shape[1] >= 26:
            if hand.longest_suit.name == "C":
                return "3C"
            if hand.longest_suit.name == "D":
                return "3D"
            if hand.longest_suit.name == "H":
                return "3H"
            if hand.longest_suit.name == "S":
                return "3S"

        # Transfers
        if hand.hcp <= 9 and hand.hearts >= 5 and hand.spades <= hand.hearts:
            return "2D"
        if hand.hcp <= 9 and hand.spades >= 5:
            return "2H"

        # Stayman
        if hand.hearts == 4 or hand.spades == 4:
            return "2C"

        # Invitational
        if 8 <= hand.hcp <= 10:
            return "2NT"

        # Game sign off
        if hand.hcp <= 17 and hand.shape[0] <= 6:
            return "3NT"

        if hand.hcp >= 22:
            return "7NT"

        if hand.hcp >= 20:
            return "6NT"

        if hand.hcp >= 17:
            return "4NT"

        return "P"


class ResponseToRebidOneNoTrump:
    @property
    def question(self) -> Question:
        """Build the question."""
        hand = self._get_hand()
        return Question(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=self._build_preamble(hand),
            question=txt.WHAT_IS_YOUR_BID,
            options=None,
            correct_response=self._correct_reponse(hand).upper(),
        )

    def _build_preamble(self, hand: Hand) -> str:
        return (
            f"Partner has opened 1C and rebid 1NT and you hold {hand_shape(hand)} "
            f"and have {hand.hcp} points"
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
            return board.hands["S"]

    def _correct_reponse(self, hand: Hand) -> str:
        return "P"


def question() -> Question:
    classes = [
        # ResponsesToOneClub(),
        # ResponsesToOneNoTrumps(),
        ResponseToRebidOneNoTrump(),
    ]
    return random.choice(classes).question
