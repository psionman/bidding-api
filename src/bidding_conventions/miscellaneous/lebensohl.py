import random

from bridgeobjects import SUITS

from bidding_conventions.bidding import stoppers_in_bid_suits
from bidding_conventions.common import get_bid_suppression
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import (
    Hand,
    one_nt_openers_hand,
)
from bidding_conventions.question import Question
from bidding_conventions.text import Text

txt = Text()

CONVENTION_TITLE = "Lebensohl"
CONVENTION_DESCRIPTION = get_description("lebensohl.html")


class ResponseToOneNt:
    @property
    def question(self) -> Question:
        global last_response
        # holding, correct_response = _random_holding()
        # points = (9, 18)
        hand = one_nt_openers_hand(dealer="S")
        overcall = random.choice(["2D", "2H", "2S", "2NT"])
        correct_response = self._get_correct_response(hand, [overcall])
        auction = ["1NT", overcall, "cursor"]
        print(f"correct_response: {correct_response}")
        bid_suppression = get_bid_suppression(auction)
        print(bid_suppression)
        return Question(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=txt.WHAT_IS_YOUR_BID,
            correct_response=correct_response,
            display_elements=["preamble", "auction", "hand"],
            auction=auction,
            hand_cards=hand.sorted_card_names,
            dealer=hand.dealer,
            vulnerability=hand.vulnerability,
            bid_suppression=bid_suppression,
        )

    def _get_correct_response(
        self, hand: Hand, opponents_bids: list[str]
    ) -> str:
        overcaller_suit = opponents_bids[0][1]
        stoppers = stoppers_in_bid_suits(hand, opponents_bids)

        if 11 <= hand.hcp and hand.is_balanced:
            if stoppers:
                return "2NT"
            else:
                return "3NT"

        suit = hand.longest_suit.name
        suits = list(SUITS)
        if hand.hcp <= 12 and hand.shape[0] >= 5:
            if suit == overcaller_suit:
                return "P"
            elif overcaller_suit in suits and suits.index(suit) > suits.index(
                overcaller_suit
            ):
                return f"2{suit}"
            else:
                return "2NT"

        if hand.hcp <= 9 and hand.shape[0] >= 6:
            if suit == overcaller_suit:
                return "P"
            elif overcaller_suit in suits and suits.index(suit) > suits.index(
                overcaller_suit
            ):
                print(f"suit: {suit}, overcaller_suit: {overcaller_suit}")
                return f"2{suit}"
            else:
                return "2NT"
        return "P"


def question() -> Question:
    classes = [
        ResponseToOneNt(),
        # AdvancersBid(),
        # AdvancerInterpretation(),
    ]
    return random.choice(classes).question


last_response = None
