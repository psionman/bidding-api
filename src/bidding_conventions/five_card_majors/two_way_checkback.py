# five_card_majors/two_way_checkback.py
import random

from bridgeobjects import Hand

from bidding_conventions.challenge import Challenge, randomize_reponses
from bidding_conventions.common import suit_html
from bidding_conventions.convention import NextQuestion
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


class TwoWayCheckbackClubs:
    @property
    def challenge(self) -> Challenge:
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
        openers_bid = random.choice(["1C", "1D"])
        responders_bid = random.choice(["1H", "1S"])
        responders_rebids = {
            "P": self._responder_passes,
            "2H": self._responder_bids_two_major,
            "2S": self._responder_bids_two_major,
            "3H": self._responder_bids_three_major,
            "3S": self._responder_bids_three_major,
        }
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
            "2C",
            "P",
            "2D",
            "P",
            responders_rebid,
        ]
        return auction, options, options[correct_response]

    def _responder_passes(self, *args) -> tuple[list[str], str]:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        return randomize_reponses(
            [
                f"To play in {DIAMONDS}",
                "Wait to see what opponents bid",
                "If opponents bid, asking you to double",
                (
                    "If opponents bid, asking you to bid 2NT with "
                    "a stop in their suit"
                ),
                f"If opponents bid, asking you to bid {responders_suit}",
            ],
            0,
        )

    def _responder_bids_two_major(self, *args) -> tuple[list[str], str]:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        responders_rebid = args[1]
        responders_rebid_suit = suit_html(responders_rebid[1])
        if responders_suit == responders_rebid_suit:
            return randomize_reponses(
                [
                    f"{txt.INV.capitalize()} with 5{responders_suit}",
                    f"{txt.INV.capitalize()} with 6{responders_suit}",
                    f"To play in {responders_suit}",
                    f"Slam try in {responders_suit}",
                    f"{txt.GF.capitalize()}",
                ],
                0,
            )
        elif responders_suit == HEARTS:
            return randomize_reponses(
                [
                    f"{txt.INV.capitalize()} with 4+{HEARTS} and 4{SPADES}",
                    f"{txt.INV.capitalize()} with 6{HEARTS}",
                    f"To play in {SPADES}",
                    f"Slam try in {HEARTS}",
                    f"{txt.GF.capitalize()}",
                ],
                0,
            )
        elif responders_suit == SPADES:
            return randomize_reponses(
                [
                    f"{txt.INV.capitalize()} with 4{HEARTS} and 5{SPADES}",
                    f"{txt.INV.capitalize()} with 6{SPADES}",
                    f"To play in {HEARTS}",
                    f"Slam try in {SPADES}",
                    f"{txt.GF.capitalize()}",
                ],
                0,
            )

    def _responder_bids_three_major(self, *args) -> tuple[list[str], str]:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        responders_rebid = args[1]
        responders_rebid_suit = suit_html(responders_rebid[1])
        other_major = _other_major(responders_rebid_suit)
        responses = [
            f"{txt.INV.capitalize()} with 6{responders_rebid_suit}",
            f"{txt.INV.capitalize()} with 5{responders_rebid_suit}/5{other_major}",
            f"To play in {responders_rebid_suit}",
            f"To play in {other_major}",
            f"Slam try in {responders_rebid_suit}",
            f"Slam try in {other_major}",
            f"{txt.GF.capitalize()}",
        ]
        if responders_suit == responders_rebid_suit:
            correct = 0
        else:
            correct = 1
        return randomize_reponses(responses, correct)


class TwoWayCheckbackDiamonds:
    @property
    def challenge(self) -> Challenge:
        self.auction, options, correct_response = self._auction_and_response()
        return Challenge(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_DOES_PARTNERS_BID_MEAN,
            display_elements=["auction"],
            options=options,
            correct_response=correct_response,
            auction=self.auction,
        )

    def _auction_and_response(self) -> tuple[list[str], str]:
        openers_bid = random.choice(["1C", "1D"])
        responders_bid = random.choice(["1H", "1S"])
        openers_rebids = {
            "2H": self._opener_bids_two_major,
            "2S": self._opener_bids_two_major,
            "2NT": self._opener_bids_two_nt,
            "3C": self._opener_bids_three_minor,
            "3D": self._opener_bids_three_minor,
        }
        openers_rebid = random.choice(list(openers_rebids.keys()))
        options, correct_response = openers_rebids[openers_rebid](
            responders_bid, openers_rebid
        )
        auction = [
            "P",
            "P",
            openers_bid,
            "P",
            responders_bid,
            "P",
            "1NT",
            "P",
            "2D",
            "P",
            openers_rebid,
        ]
        return auction, options, options[correct_response]

    def _opener_bids_two_major(self, *args) -> tuple[list[str], str]:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        openers_bid = args[1]
        openers_suit = suit_html(openers_bid[1])
        other_major = _other_major(openers_suit)

        responses = [
            f"3+{openers_suit} game force",
            f"4+{openers_suit} (denies 3{other_major}); {txt.GF}",
            f"3+{openers_suit} {txt.INV}",
            f"4+{openers_suit} (denies 3{other_major}) {txt.INV}",
            f"Asking for a stop in {openers_suit}; {txt.GF}",
            f"Promising a stop in {openers_suit}; {txt.GF}",
        ]
        correct = 0 if responders_suit == openers_suit else 1
        return randomize_reponses(responses, correct)

    def _opener_bids_two_nt(self, *args) -> tuple[list[str], str]:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        other_major = _other_major(responders_suit)

        responses = [
            f"Denies 3{responders_suit} and 4{other_major}; {txt.GF}",
            f"Denies 3{responders_suit} and 4{other_major}; {txt.INV}",
            "To play",
            f"Asking for stop in {other_major}; {txt.GF}",
            f"Promising stop in {other_major}; {txt.GF}",
            f"Asking you to bid 3{CLUBS}",
        ]
        return randomize_reponses(responses, 0)

    def _opener_bids_three_minor(self, *args) -> tuple[list[str], str]:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        openers_bid = args[1]
        openers_suit = suit_html(openers_bid[1])
        other_major = _other_major(responders_suit)

        responses = [
            (
                f"Denies 3{responders_suit} and 4{other_major} "
                f"but 5 good {openers_suit}; {txt.GF}"
            ),
            f"Denies 3{responders_suit} and 4{other_major}; {txt.INV}",
            "To play",
            f"Asking for stop in {openers_suit}; {txt.GF}",
            f"Promising stop in {openers_suit}; {txt.GF}",
            f"Promising stop in {openers_suit}; {txt.INV}",
        ]
        return randomize_reponses(responses, 0)


class OpenersInterpretationNoCheckback:
    @property
    def challenge(self) -> Challenge:
        hand = self._get_hand()
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
            vulnerability=hand.vulnerability,
        )

    def _auction_and_response(self) -> tuple[list[str], str]:
        openers_bid = random.choice(["1C", "1D"])
        responders_bid = random.choice(["1H", "1S"])
        responders_rebids = {
            "2H": self._responder_bids_two_hearts,
            "2S": self._responder_bids_two_spades,
            "2NT": self._responder_bids_two_nt,
            "3C": self._responder_bids_three_suit,
            "3D": self._responder_bids_three_suit,
            "3H": self._responder_bids_three_suit,
            "3S": self._responder_bids_three_suit,
            "3NT": self._responder_bids_game,
            "4H": self._responder_bids_game,
            "4S": self._responder_bids_game,
            "4NT": self._responder_bids_four_nt,
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

    def _responder_bids_two_hearts(self, *args) -> tuple[list[str], str]:
        return randomize_reponses(
            [
                f"Promises 6{HEARTS} {txt.INV} mute on {SPADES} holding",
                f"Promises 6{HEARTS} {txt.INV} denies 4{SPADES}",
                f"Promises 6{HEARTS} {txt.INV} promises 4{SPADES}",
                f"Promises 6{HEARTS} forcing",
                f"Promises stop in {HEARTS}",
                f"Asking for stop in {HEARTS}",
                f"Transfer to {SPADES}",
                f"Game force in {HEARTS}",
                f"Slam try in {HEARTS}",
            ],
            0,
        )

    def _responder_bids_two_spades(self, *args) -> tuple[list[str], str]:
        return randomize_reponses(
            [
                f"Promises 6{SPADES} {txt.INV} denies 4{HEARTS}",
                f"Promises 6{SPADES} {txt.INV} promises 4{HEARTS}",
                f"Promises 6{SPADES} {txt.INV} mute on {HEARTS} holding",
                f"Promises 6{SPADES} forcing",
                f"Promises stop in {SPADES}",
                f"Asking for stop in {SPADES}",
                f"Game force in {SPADES}",
                f"Slam try in {SPADES}",
            ],
            0,
        )

    def _responder_bids_two_nt(self, *args) -> tuple[list[str], str]:
        responders_bid = args[0]
        responders_suit = suit_html(responders_bid[1])
        return randomize_reponses(
            [
                f"{txt.INV.capitalize()}",
                f"{txt.INV.capitalize()} promises stop in {responders_suit}",
                f"{txt.INV.capitalize()} asking for stop in {responders_suit}",
                f"{txt.GF.capitalize()}",
                f"Asking partner to bid 3{CLUBS}",
            ],
            0,
        )

    def _responder_bids_three_suit(self, *args) -> tuple[list[str], str]:
        first_suit = suit_html(args[0][1])
        second_suit = suit_html(args[1][1])
        common_responses = [
            f"Promising stop in {second_suit}",
            f"Asking for stop in {second_suit}",
            f"Takeout, promises 6{second_suit}",
            f"{txt.GF.capitalize()}",
            f"{txt.INV.capitalize()}",
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

    def _responder_bids_game(self, *args) -> tuple[list[str], str]:
        return randomize_reponses(
            ["To play", f"{txt.INV.capitalize()}", "Slam try", "Forcing"],
            0,
        )

    def _responder_bids_four_nt(self, *args) -> tuple[list[str], str]:
        return randomize_reponses(
            ["To play", f"{txt.INV.capitalize()}", "Slam try", "Forcing"],
            0,
        )

    def _get_hand(self) -> Hand:
        points = (12, 15)
        holding = {"S": 5}
        hand = one_nt_overcaller_hand(holding, points)
        return hand


class OpenersInterpretationWithCheckback:
    @property
    def challenge(self) -> Challenge:
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
        openers_bid = random.choice(["1C", "1D"])
        responders_bid = random.choice(["1H", "1S"])
        responders_rebids = {
            "2C": self._responder_bids_two_clubs,
            "2D": self._responder_bids_two_diamonds,
        }
        responders_rebid = random.choice(list(responders_rebids.keys()))
        options, correct_response = responders_rebids[responders_rebid]()
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

    def _responder_bids_two_clubs(self, *args) -> tuple[list[str], str]:
        return randomize_reponses(
            [
                f"Asks partner to bid 2{DIAMONDS}",
                f"Slam try in {CLUBS}",
                f"To play in {CLUBS}",
                f"Asking for stop in {CLUBS}",
                f"Promising stop in {CLUBS}",
                f"Transfer to {DIAMONDS}",
                f"{txt.INV.capitalize()}",
                f"{txt.GF.capitalize()}",
            ],
            0,
        )

    def _responder_bids_two_diamonds(self, *args) -> tuple[list[str], str]:
        return randomize_reponses(
            [
                f"{txt.GF.capitalize()}",
                f"Slam try in {DIAMONDS}",
                f"To play in {DIAMONDS}",
                f"Asking for stop in {DIAMONDS}",
                f"Promising stop in {DIAMONDS}",
                f"Transfer to {HEARTS}",
                f"{txt.INV.capitalize()}",
            ],
            0,
        )


def _other_major(suit: str) -> str:
    if suit == HEARTS:
        return SPADES
    return HEARTS


QUESTION_CLASSES: list[tuple[type, int]] = [
    (TwoWayCheckbackClubs, 1),
    (TwoWayCheckbackDiamonds, 1),
    (OpenersInterpretationNoCheckback, 1),
    (OpenersInterpretationWithCheckback, 1),
]


challenge = NextQuestion(QUESTION_CLASSES).challenge
