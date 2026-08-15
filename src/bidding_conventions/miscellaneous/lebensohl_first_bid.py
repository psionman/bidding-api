import dataclasses
import hashlib
import random

from bridgeobjects import SUITS as SUITS_CONST

from bidding_conventions.bidding import stoppers_in_bid_suits
from bidding_conventions.common import get_bid_suppression, suit_html
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import (
    Hand,
    display_hand,
    one_nt_lebensohl_hand,
    one_nt_openers_hand,
    weak_two_opener,
)
from bidding_conventions.question import Question
from bidding_conventions.text import Text

txt = Text()

CONVENTION_TITLE = "Lebensohl"
CONVENTION_DESCRIPTION = get_description("lebensohl.html")

SUITS = list(SUITS_CONST)


class Responder:
    def __init__(self):
        self.auction = None
        self.opponents_bid = None
        self.dealer = None
        self.hand = None

    @property
    def correct_response(self) -> str:
        return self._responders_first_bid(self.hand, self.auction)

    @property
    def is_forcing(self) -> bool:
        return self.auction[2] == "P" and self.auction[1] == "D"

    @property
    def question(self) -> Question:
        global last_response
        correct_response = self._responders_first_bid(
            self.hand, self.opponents_bid
        )
        print(self.auction, correct_response)
        print("=" * 30)

        bid_suppression = get_bid_suppression(self.auction)
        return Question(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=txt.WHAT_IS_YOUR_BID,
            correct_response=correct_response,
            display_elements=["preamble", "auction", "hand"],
            auction=self.auction,
            hand_cards=self.hand.sorted_card_names,
            dealer=self.dealer,
            vulnerability=self.hand.vulnerability,
            bid_suppression=bid_suppression,
        )

    def _responders_first_bid(self, hand: Hand, opponents_bid: str) -> str:
        opponent_suit = opponents_bid[1]
        suit = hand.longest_suit.name
        # Very weak hands
        if hand.hcp <= 5 and hand.shape[0] <= 4 and not self.is_forcing:
            return "P"

        # Longest suit is the same as opponent's suit
        if suit == opponent_suit:
            return self._has_opponent_suit(suit, opponent_suit)

        # competitive
        if hand.hcp <= 9:
            return self._competitive_bids(suit, opponent_suit)

        # Invitational
        if 10 <= hand.hcp <= 11:
            return self._invitational_bids(suit, opponent_suit)

        # Game forcing
        return self._game_forcing_bids(suit, opponent_suit)

    def _has_opponent_suit(self, suit: str, opponent_suit: str) -> str:
        # Longest suit is the same as opponent's suit
        if self.hand.hcp >= 9 and not self.is_forcing:
            return "D"
        return "P"

    def _competitive_bids(self, suit: str, opponent_suit: str) -> str:

        if self.hand.hcp <= 5 and self.hand.shape[0] >= 5:
            if self._barrier_broken(suit, opponent_suit):
                return f"2{suit}"
            if not self.is_forcing:
                return "P"
            return "2NT"

        if self._barrier_broken(suit, opponent_suit):
            return f"2{suit}"
        return "2NT"

    def _invitational_bids(self, suit: str, opponent_suit: str) -> str:
        if self._barrier_broken(suit, opponent_suit):
            return f"3{suit}"
        return "2NT"

    def _game_forcing_bids(self, suit: str, opponent_suit: str) -> str:
        hand = self.hand
        stoppers = stoppers_in_bid_suits(hand, [f"2{opponent_suit}"])
        if hand.is_balanced:
            if stoppers:
                return "2NT"
            else:
                return "3NT"

        if self._barrier_broken(suit, opponent_suit):
            return f"3{hand.longest_suit.name}"
        if not stoppers:
            if hand.four_card_major_or_better:
                return f"3{opponent_suit}"
        return "3NT"

    def _barrier_broken(self, suit: str, opponent_suit: str) -> bool:
        return SUITS.index(suit) > SUITS.index(opponent_suit)


class ResponseToOneNt(Responder):
    def __init__(self):
        super().__init__()
        self.opponents_bid = random.choice(["2D", "2H", "2S"])
        self.dealer = "S"
        self.auction = ["1NT", self.opponents_bid, "cursor"]
        while True:
            self.hand = one_nt_lebensohl_hand(
                {self.opponents_bid[1]: 6}, [10, 15]
            )
            if len(self.hand.cards_by_suit[self.opponents_bid[1]]) > 3:
                continue
            break


class ResponseToWeakTwoDoubled(Responder):
    def __init__(self):
        super().__init__()
        self.opponents_bid = random.choice(["2D", "2H", "2S"])
        self.dealer = "E"
        while True:
            self.hand = weak_two_opener()
            if len(self.hand.cards_by_suit[self.opponents_bid[1]]) > 3:
                continue
            break
        self.auction = self.hand.auction
        display_hand(self.hand)


@dataclasses.dataclass
class Response:
    overcall: str
    response: str
    options: list[str]
    correct_response: int
    hash_id: str = dataclasses.field(init=False, repr=False)

    def __post_init__(self) -> None:
        payload = "|".join(
            [
                self.overcall,
                self.response,
                *self.options,
                str(self.correct_response),
            ]
        )
        self.hash_id = hashlib.sha256(payload.encode()).hexdigest()


class OpenersInterpretationDirect:
    def __init__(self):
        self.options = self._get_options()

    @property
    def question(self) -> Question:
        global last_response
        while True:
            response = random.choice(self.options)
            if response.hash_id == last_response:
                continue
            break
        last_response = response.hash_id

        hand = one_nt_openers_hand(dealer="S")  # used for vulnerability
        correct_response = response.options[response.correct_response]
        auction = ["1NT", response.overcall, response.response, "P", "cursor"]
        return Question(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=txt.WHAT_DOES_PARTNERS_BID_MEAN,
            options=response.options,
            correct_response=correct_response,
            display_elements=["preamble", "auction"],
            auction=auction,
            dealer="N",
            vulnerability=hand.vulnerability,
        )

    def _get_options(self) -> list[Response]:
        options = []
        options.extend(self._partner_bids_two_major())
        options.extend(self._partner_bids_two_nt())
        options.extend(self._partner_bids_three())
        options.extend(self._partner_bids_three_major())
        options.extend(self._partner_cue_bids())
        options.extend(self._partner_bids_three_nt())
        return options

    def _partner_bids_two_major(self) -> list[Response]:
        responses = []

        overcall_suit = "D"
        for suit in ["H", "S"]:
            responders_suit = suit_html(suit)
            (options, correct_response) = self._randomize_options(
                self._two_major_responses(responders_suit, overcall_suit),
                0,
            )
            response = Response(
                overcall=f"2{overcall_suit}",
                response=f"2{suit}",
                options=options,
                correct_response=correct_response,
            )
            responses.append(response)

        overcall_suit = "H"
        responders_suit = suit_html("S")
        response = Response(
            f"2{overcall_suit}",
            "2S",
            self._two_major_responses(responders_suit, overcall_suit),
            0,
        )
        responses.append(response)
        return responses

    def _two_major_responses(self, suit: str, overcall_suit: str) -> list[str]:
        return [
            f"To play in {suit}",
            f"Invitational in {suit}",
            f"Game Force in {suit}",
            f"Asking for stop in {suit}",
            f"Asking you to bid 2NT with stop in {suit_html(overcall_suit)}",
            f"Asking you to bid 3{suit_html(overcall_suit)}",
        ]

    def _partner_bids_two_nt(self) -> list[Response]:
        responses = []
        for opponent_suit in ["D", "H", "S"]:
            (options, correct_response) = self._randomize_options(
                [
                    f"Asking partner to bid 3{suit_html('C')}",
                    "Asking partner to Pass",
                    "Asking partner to bid 3NT",
                    f"Asking partner to bid 3{suit_html(opponent_suit)}",
                ],
                0,
            )
            response = Response(
                overcall=f"2{opponent_suit}",
                response="2NT",
                options=options,
                correct_response=correct_response,
            )
            responses.append(response)
        return responses

    def _partner_bids_three(self) -> list[Response]:
        responses = []

        suits = list(SUITS)
        for overcall_suit in ["D", "H", "S"]:
            while True:
                responders_suit = random.choice(["C", "D", "H"])
                if responders_suit == overcall_suit or suits.index(
                    responders_suit
                ) > suits.index(overcall_suit):
                    continue
                break
            suit = suit_html(responders_suit)
            (options, correct_response) = self._randomize_options(
                [
                    f"Invitational; (promises 5+ {suit}s)",
                    f"To play in {suit}",
                    f"Game Force in {suit}",
                    f"Asking for stop in {suit}",
                    f"Asking you to bid 3NT with stop in {suit_html(overcall_suit)}",
                ],
                0,
            )
            response = Response(
                overcall=f"2{overcall_suit}",
                response=f"3{responders_suit}",
                options=options,
                correct_response=correct_response,
            )
            responses.append(response)

        return responses

    def _partner_bids_three_major(self) -> list[Response]:
        responses = []

        suits = list(SUITS)
        for overcall_suit in ["D", "H"]:
            while True:
                responders_suit = random.choice(["H", "S"])

                if suits.index(responders_suit) <= suits.index(overcall_suit):
                    # if responders_suit == overcall_suit:
                    continue
                break
            suit = suit_html(responders_suit)
            (options, correct_response) = self._randomize_options(
                [
                    f"Game Force (promises 5+ {suit}s)",
                    f"Invitational in {suit}",
                    f"To play in {suit}",
                    f"Asking for stop in {suit}",
                    f"Asking you to bid 3NT with stop in {suit_html(overcall_suit)}",
                ],
                0,
            )
            response = Response(
                overcall=f"2{overcall_suit}",
                response=f"3{responders_suit}",
                options=options,
                correct_response=correct_response,
            )
            responses.append(response)

        return responses

    def _partner_cue_bids(self) -> list[Response]:
        responses = []

        for overcall_suit in ["D", "H", "S"]:
            responders_suit = overcall_suit
            suit = suit_html(overcall_suit)
            (options, correct_response) = self._randomize_options(
                [
                    f"Forcing; denies stop in {suit}, promises 4+ card major",
                    f"Forcing; promises stop in {suit}, promises 4+ card major",
                    f"Forcing; denies stop in {suit}, denies 4+ card major",
                    f"Forcing; promises stop in {suit}, denies 4+ card major",
                    f"Forcing; no stop in {suit}",
                    f"Invitational in {suit} (promises 6+ cards)",
                    f"To play in {suit}",
                    f"Asking for stop in {suit}",
                    f"Asking you to bid 3NT with stop in {suit}",
                ],
                0,
            )
            response = Response(
                overcall=f"2{overcall_suit}",
                response=f"3{responders_suit}",
                options=options,
                correct_response=correct_response,
            )
            responses.append(response)

        return responses

    def _partner_bids_three_nt(self) -> list[Response]:
        responses = []

        for overcall_suit in ["D", "H", "S"]:
            suit = suit_html(overcall_suit)
            (options, correct_response) = self._randomize_options(
                [
                    f"Pass or correct; denies stop in {suit}, denies a 4-card major",
                    f"Pass or correct; promises stop in {suit}, denies a 4-card major",
                    f"Pass or correct; denies stop in {suit}, promises a 4-card major",
                    f"Pass or correct; promises stop in {suit}, promises a 4-card major",
                    f"Invitational in {suit} (promises 6+ cards)",
                    f"To play in {suit}",
                    f"Asking for stop in {suit}",
                ],
                0,
            )
            response = Response(
                overcall=f"2{overcall_suit}",
                response="3NT",
                options=options,
                correct_response=correct_response,
            )
            responses.append(response)

        return responses

    def _randomize_options(
        self, options: list[str], correct_response: int
    ) -> list[str]:
        correct_option = options[correct_response]
        shuffled = random.sample(options, k=len(options))
        correct_index = shuffled.index(correct_option)
        return shuffled, correct_index


def question() -> Question:
    classes = [
        ResponseToOneNt(),
        ResponseToWeakTwoDoubled(),
        OpenersInterpretationDirect(),
    ]
    return random.choice(classes).question


last_response = None
