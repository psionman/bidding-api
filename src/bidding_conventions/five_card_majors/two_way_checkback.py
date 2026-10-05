# /five_card_majors/two_way_checkback.py
import random

from bridgeobjects import Hand

from bidding_conventions.challenge import Challenge
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import one_nt_overcaller_hand
from bidding_conventions.text import Text

txt = Text()

CONVENTION_THEME = "5 Card Majors"
CONVENTION_TITLE = "Two Way Checkback"
CONVENTION_DESCRIPTION = get_description("fcm_opening.html")


class TwoWayCheckback:
    @property
    def challenge(self) -> Challenge:
        """Build the question."""
        hand = self._get_hand()
        return Challenge(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_YOUR_BID,
            hand_cards=hand.sorted_card_names,
            display_elements=["auction", "hand"],
            correct_response=self._correct_reponse(hand).upper(),
        )

    def _get_hand(self) -> Hand:
        points = (12, 15)
        holding = {"S": 5}
        hand = one_nt_overcaller_hand(holding, points)
        return hand

    def _correct_reponse(self, hand: Hand) -> str:
        return "2C"


def challenge() -> Challenge:
    challenges = [
        TwoWayCheckback(),
    ]
    return random.choice(challenges).challenge
