# five_card_majors/two_way_checkback.py
import random

from bridgeobjects import Hand

from bidding_conventions.challenge import Challenge, randomize_reponses
from bidding_conventions.common import suit_html
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import one_nt_overcaller_hand
from bidding_conventions.text import Text

txt = Text()

CONVENTION_THEME = "5 Card Majors"
CONVENTION_TITLE = "Two Way Checkback"
CONVENTION_DESCRIPTION = get_description("fcm_opening.html")

HEARTS = suit_html("H")
SPADES = suit_html("S")
CLUBS = suit_html("C")
DIAMONDS = suit_html("D")


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
            display_elements=["auction", "hand", "bidding_box"],
            correct_response=self._correct_reponse(hand).upper(),
        )

    def _get_hand(self) -> Hand:
        points = (12, 15)
        holding = {"S": 5}
        hand = one_nt_overcaller_hand(holding, points)
        return hand

    def _correct_reponse(self, hand: Hand) -> str:
        return "2C"


class OpenersInterpretationNoCheckback:
    @property
    def challenge(self) -> Challenge:
        """Build the question."""
        auction, options, correct_response = self._auction_and_response()
        return Challenge(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_DOES_PARTNERS_BID_MEAN,
            display_elements=["auction"],
            options=options,
            correct_response=correct_response,
            auction=auction,
        )

    def _auction_and_response(self) -> tuple[list[str], str]:
        # Build auction and response
        openers_bid = random.choice(["1C", "1D"])
        responders_bid = random.choice(["1H", "1S"])
        responders_rebids = {
            "2H": self._partner_bids_two_hearts,
            "2S": self._partner_bids_two_spades,
            "2NT": self._partner_bids_two_nt,
            "3C": self._partner_bids_three_suit,
            "3D": self._partner_bids_three_suit,
            "3H": self._partner_bids_three_suit,
            "3S": self._partner_bids_three_suit,
            "3NT": self._partner_bids_game,
            "4H": self._partner_bids_game,
            "4S": self._partner_bids_game,
            "4NT": self._partner_bids_four_nt,
        }
        if responders_bid == "1H":
            responders_rebids.pop("2S")
            responders_rebids.pop("4S")
        if responders_bid == "1S":
            responders_rebids.pop("2H")
            responders_rebids.pop("4H")
        responders_rebid = random.choice(list(responders_rebids.keys()))
        options, correct_response = responders_rebids[responders_rebid](
            responders_bid, responders_rebid
        )
        auction = [
            openers_bid,
            "P",
            responders_bid,
            "P",
            "1NT",
            "P",
            responders_rebid,
        ]
        return auction, options, options[correct_response]

    def _partner_bids_two_hearts(self, *args) -> None:
        return randomize_reponses(
            [
                f"Promises 6{HEARTS} invitational mute on {SPADES} holding",
                f"Promises 6{HEARTS} invitational denies 4{SPADES}",
                f"Promises 6{HEARTS} invitational promises 4{SPADES}",
                f"Promises 6{HEARTS} forcing",
                f"Promises stop in {HEARTS}",
                f"Asking for stop in {HEARTS}",
                f"Transfer to {SPADES}",
                f"Game force in {HEARTS}",
                f"Slam try in {HEARTS}",
            ],
            0,
        )

    def _partner_bids_two_spades(self, *args) -> None:
        return randomize_reponses(
            [
                f"Promises 6{SPADES} invitational denies 4{HEARTS}",
                f"Promises 6{SPADES} invitational promises 4{HEARTS}",
                f"Promises 6{SPADES} invitational mute on {HEARTS} holding",
                f"Promises 6{SPADES} forcing",
                f"Promises stop in {SPADES}",
                f"Asking for stop in {SPADES}",
                f"Game force in {SPADES}",
                f"Slam try in {SPADES}",
            ],
            0,
        )

    def _partner_bids_two_nt(self, *args) -> None:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        return randomize_reponses(
            [
                "Invitational",
                f"Invitational promises stop in {responders_suit}",
                f"Invitational askiing for stop in {responders_suit}",
                "Game forcing",
                f"Asking partner to bid 3{CLUBS}",
            ],
            0,
        )

    def _partner_bids_three_suit(self, *args) -> None:
        first_suit = suit_html(args[0][1])
        second_suit = suit_html(args[1][1])
        common_responses = [
            f"Promising stop in {second_suit}",
            f"Asking for stop in {second_suit}",
            f"Takeout, promises 6{second_suit}",
            "Game forcing",
            "Invitational",
        ]
        if first_suit == second_suit:
            responses = [f"slam try in {first_suit}"]
        else:
            responses = [f"Slam try 5/5 in {first_suit} and {second_suit}"]
        responses.extend(common_responses)
        return randomize_reponses(
            responses,
            0,
        )

    def _partner_bids_game(self, *args) -> None:
        return randomize_reponses(
            ["To play", "Invitational", "Slam try", "Forcing"],
            0,
        )

    def _partner_bids_four_nt(self, *args) -> None:
        return randomize_reponses(
            ["To play", "Invitational", "Slam try", "Forcing"],
            0,
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
        # TwoWayCheckback(),
        OpenersInterpretationNoCheckback(),
    ]
    return random.choice(challenges).challenge
