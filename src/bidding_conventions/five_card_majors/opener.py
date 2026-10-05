# five_card_majors/opener.py

import random

# from bfgdealer.dealer_solo import Dealer
from bridgeobjects import BALANCED_SHAPES, Hand

from bidding_conventions.challenge import Challenge
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import opening_one_hand

CONVENTION_THEME = "5 Card Majors"
CONVENTION_TITLE = "Opener's bids"
CONVENTION_DESCRIPTION = get_description("fcm_opening.html")
from bidding_conventions.text import Text

txt = Text()


class Opener:
    @property
    def challenge(self) -> Challenge:
        """
        Build the question.
        """
        hand = opening_one_hand()
        correct = self._correct_reponse(hand).upper()
        return Challenge(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_YOUR_BID,
            options=None,
            correct_response=correct,
            hand_cards=hand.sorted_card_names,
            vulnerability=hand.vulnerability,
            dealer=hand.dealer,
            auction=hand.auction + ["cursor"],
            display_elements=["hand", "auction", "bidding_box"],
        )

    def _correct_reponse(self, hand: Hand) -> str:
        if 15 <= hand.hcp <= 17 and hand.shape in BALANCED_SHAPES:
            return "1NT"
        if hand.hearts >= 5 and hand.spades <= hand.hearts:
            return "1H"
        if hand.spades >= 5 and hand.spades > hand.hearts:
            return "1S"
        if hand.diamonds >= 4 and hand.diamonds > hand.clubs:
            return "1D"
        return "1C"


def challenge() -> Challenge:
    classes = [
        Opener(),
    ]
    return random.choice(classes).question
