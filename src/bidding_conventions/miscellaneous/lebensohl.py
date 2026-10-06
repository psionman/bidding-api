# lebensohl.py
import dataclasses
import hashlib
import random

from bridgeobjects import SUITS

from bidding_conventions.bidding import stoppers_in_bid_suits
from bidding_conventions.challenge import Challenge, randomize_reponses
from bidding_conventions.common import get_bid_suppression, suit_html
from bidding_conventions.convention import NextQuestion
from bidding_conventions.descriptions import get_description
from bidding_conventions.hand import (
    Hand,
    one_nt_lebensohl_hand,
    one_nt_openers_hand,
    weak_two_opener,
)
from bidding_conventions.text import Text

txt = Text()

CONVENTION_THEME = "Lebensohl"
CONVENTION_DESCRIPTION = get_description("lebensohl.html")

SUIT_ORDER = {suit: i for i, suit in enumerate(list(SUITS))}


@dataclasses.dataclass
class Response:
    opponents_bid: str
    response: str
    options: list[str]
    correct_response_index: int
    hash_id: str = dataclasses.field(init=False, repr=False)

    def __post_init__(self) -> None:
        payload = "|".join(
            [
                self.opponents_bid,
                self.response,
                *self.options,
                str(self.correct_response_index),
            ]
        )
        self.hash_id = hashlib.sha256(payload.encode()).hexdigest()


class RespondersBid:
    def __init__(self):
        self.opponents_bid: str = ""
        self.auction: list[str] = []
        self.dealer: str = ""
        self.hand: Hand = None

    @property
    def challenge(self) -> Challenge:
        correct_response = self._responders_first_bid(
            self.hand, self.opponents_bid
        )

        bid_suppression = get_bid_suppression(self.auction)
        return Challenge(
            theme=CONVENTION_THEME,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_YOUR_BID,
            correct_response=correct_response,
            display_elements=["auction", "hand", "bidding_box"],
            auction=self.auction,
            hand_cards=self.hand.sorted_card_names,
            dealer=self.dealer,
            vulnerability=self.hand.vulnerability,
            bid_suppression=bid_suppression,
        )

    @property
    def is_forcing(self) -> bool:
        return self.auction[2] == "P" and self.auction[1] == "D"

    def _responders_first_bid(self, hand: Hand, opponents_bid: str) -> str:
        opponents_suit = opponents_bid[1]
        suit = hand.longest_suit.name
        # Very weak hands
        if hand.hcp <= 5 and hand.shape[0] <= 4 and not self.is_forcing:
            return "P"

        # Longest suit is the same as opponent's suit
        if suit == opponents_suit:
            return self._has_opponent_suit(suit, opponents_suit)

        # competitive
        if hand.hcp <= 9:
            return self._competitive_bids(suit, opponents_suit)

        # Invitational
        if 10 <= hand.hcp <= 11:
            return self._invitational_bids(suit, opponents_suit)

        # Game forcing
        return self._game_forcing_bids(suit, opponents_suit)

    def _has_opponent_suit(self, suit: str, opponents_suit: str) -> str:
        # Longest suit is the same as opponent's suit
        if self.hand.hcp >= 9 and not self.is_forcing:
            return "D"
        return "P"

    def _competitive_bids(self, suit: str, opponents_suit: str) -> str:

        if self.hand.hcp <= 5 and self.hand.shape[0] >= 5:
            if self._barrier_broken(suit, opponents_suit):
                return f"2{suit}"
            # TODO bid 4 cards uit at 2 level with <6 pts?
            if not self.is_forcing or suit == opponents_suit:
                return "P"
            return "2NT"

        if self._barrier_broken(suit, opponents_suit):
            return f"2{suit}"
        return "2NT"

    def _invitational_bids(self, suit: str, opponents_suit: str) -> str:
        if self._barrier_broken(suit, opponents_suit):
            return f"3{suit}"
        return "2NT"

    def _game_forcing_bids(self, suit: str, opponents_suit: str) -> str:
        hand = self.hand
        stoppers = stoppers_in_bid_suits(hand, [f"2{opponents_suit}"])
        if hand.is_balanced:
            if stoppers:
                return "2NT"
            else:
                return "3NT"

        if self._barrier_broken(suit, opponents_suit):
            return f"3{hand.longest_suit.name}"
        if not stoppers:
            if hand.four_card_major_or_better:
                return f"3{opponents_suit}"
        return "3NT"

    def _barrier_broken(self, suit: str, opponents_suit: str) -> bool:
        return SUIT_ORDER[suit] > SUIT_ORDER[opponents_suit]


class ResponseToOneNt(RespondersBid):
    def __init__(self):
        super().__init__()
        self.dealer = "S"
        self.opponents_bid = random.choice(["2C", "2D", "2H", "2S"])
        self.auction = ["1NT", self.opponents_bid, "cursor"]
        while True:
            self.hand = one_nt_lebensohl_hand(
                {self.opponents_bid[1]: 6}, [10, 15]
            )
            if len(self.hand.cards_by_suit[self.opponents_bid[1]]) > 3:
                continue
            break


class ResponseToWeakTwoDoubled(RespondersBid):
    def __init__(self):
        super().__init__()
        self.dealer = "E"
        self.opponents_bid = random.choice(["2D", "2H", "2S"])
        while True:
            self.hand = weak_two_opener()
            if len(self.hand.cards_by_suit[self.opponents_bid[1]]) > 3:
                continue
            break
        self.auction = self.hand.auction


@dataclasses.dataclass(frozen=True)
class InterpretationContext:
    overcall_suits: tuple[str, ...]
    responder_suits: tuple[str, ...]


AFTER_1NT = InterpretationContext(
    overcall_suits=("H", "S"),
    responder_suits=("D", "H", "S"),
)

AFTER_WEAK_2 = InterpretationContext(
    overcall_suits=("D", "H", "S"),
    responder_suits=("D", "H", "S"),
)


@dataclasses.dataclass
class InterpretationQuestion:
    response: Response
    auction: list[str]
    dealer: str
    vulnerability: str

    @property
    def challenge(self) -> Challenge:
        correct_response = self.response.options[
            self.response.correct_response_index
        ]

        return Challenge(
            theme=CONVENTION_THEME,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_DOES_PARTNERS_BID_MEAN,
            options=self.response.options,
            correct_response=correct_response,
            display_elements=["auction"],
            auction=self.auction,
            dealer=self.dealer,
            vulnerability=self.vulnerability,
        )


class OpenersInterpretation:
    def __init__(self, context: InterpretationContext):
        self.context = context
        responses = self._get_responses()
        self.response = random.choice(responses)
        # Subclasses must set self.auction and self.dealer, then build
        # self.question, after calling super().__init__().

    def _build_challenge(self) -> InterpretationQuestion:
        hand = one_nt_openers_hand(dealer="S")  # used for vulnerability
        return InterpretationQuestion(
            response=self.response,
            auction=self.auction,
            dealer=self.dealer,
            vulnerability=hand.vulnerability,
        )

    def _get_suits(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        return self.context.overcall_suits, self.context.responder_suits

    def _get_responses(self) -> list[Response]:
        responses = []
        responses.extend(self._partner_bids_two_nt())
        responses.extend(self._partner_bids_at_two_level())
        responses.extend(self._partner_bids_at_three_level())
        responses.extend(self._partner_cue_bids())
        responses.extend(self._partner_bids_three_nt())
        return responses

    def _partner_bids_two_nt(self) -> list[Response]:
        responses = []
        for opponents_suit in ["D", "H", "S"]:
            (options, correct_index) = randomize_reponses(
                [
                    f"Asking partner to bid 3{suit_html('C')}",
                    "Asking partner to Pass",
                    "Asking partner to bid 3NT",
                    f"Asking partner to bid 3{suit_html(opponents_suit)}",
                ],
                0,
            )
            response = Response(
                opponents_bid=f"2{opponents_suit}",
                response="2NT",
                options=options,
                correct_response_index=correct_index,
            )
            responses.append(response)
        return responses

    def _partner_bids_at_two_level(self) -> list[Response]:
        responses = []
        overcall_suits, responders_suits = self._get_suits()
        for responders_suit in responders_suits:
            for overcall_suit in overcall_suits:
                if SUIT_ORDER[responders_suit] <= SUIT_ORDER[overcall_suit]:
                    continue
                (options, correct_index) = randomize_reponses(
                    self._two_level_responses(overcall_suit, responders_suit),
                )
                responses.append(
                    Response(
                        opponents_bid=f"2{overcall_suit}",
                        response=f"2{responders_suit}",
                        options=options,
                        correct_response_index=correct_index,
                    )
                )
        return responses

    def _two_level_responses(
        self, overcall_suit: str, responders_suit: str
    ) -> list[str]:
        suit = suit_html(responders_suit)
        return [
            f"To play in {suit}",
            f"Invitational in {suit}",
            f"Game Force in {suit}",
            f"Asking for stop in {suit}",
            f"Asking you to bid 2NT with stop in {suit_html(overcall_suit)}",
            f"Asking you to bid 3{suit_html(overcall_suit)}",
        ]

    def _partner_bids_at_three_level(self) -> list[Response]:
        responses = []
        overcall_suits, responders_suits = self._get_suits()
        for responders_suit in responders_suits:
            chosen_overcall_suit = None
            for overcall_suit in overcall_suits:
                if responders_suit == overcall_suit:
                    continue
                chosen_overcall_suit = overcall_suit
                break
            if chosen_overcall_suit is None:
                continue

            (options, correct_index) = randomize_reponses(
                self._three_level_responses(
                    chosen_overcall_suit, responders_suit
                ),
            )
            response = Response(
                opponents_bid=f"2{chosen_overcall_suit}",
                response=f"3{responders_suit}",
                options=options,
                correct_response_index=correct_index,
            )
            responses.append(response)

        return responses

    def _three_level_responses(
        self, overcall_suit: str, responders_suit: str
    ) -> list[str]:
        suit = suit_html(responders_suit)
        return [
            f"Game Force; promises 5+ {suit}",
            f"Invitational; promises 5+ {suit}",
            f"To play in {suit}",
            f"Asking for stop in {suit}",
            f"Promises stop in {suit}",
            f"Denies stop in {suit}",
            f"Asking you to bid 3NT with stop in {suit_html(overcall_suit)}",
        ]

    def _partner_cue_bids(self) -> list[Response]:
        responses = []
        for overcall_suit in ["D", "H", "S"]:
            (options, correct_index) = randomize_reponses(
                self._cue_bid_responses(overcall_suit)
            )
            response = Response(
                opponents_bid=f"2{overcall_suit}",
                response=f"3{overcall_suit}",
                options=options,
                correct_response_index=correct_index,
            )
            responses.append(response)
        return responses

    def _cue_bid_responses(self, overcall_suit: str) -> list[str]:
        suit = suit_html(overcall_suit)
        return [
            f"Denies stop in {suit}; promises 4+ card major",
            f"Promises stop in {suit}; promises 4+ card major",
            f"Denies stop in {suit}; denies 4+ card major",
            f"Promises stop in {suit}; denies 4+ card major",
            f"Invitational in {suit}; promises 6+ {suit}",
            f"To play in {suit}",
            f"Asking for stop in {suit}",
        ]

    def _partner_bids_three_nt(self) -> list[Response]:
        responses = []
        for overcall_suit in ["D", "H", "S"]:
            (options, correct_index) = randomize_reponses(
                self._three_nt_options(overcall_suit)
            )
            response = Response(
                opponents_bid=f"2{overcall_suit}",
                response="3NT",
                options=options,
                correct_response_index=correct_index,
            )
            responses.append(response)
        return responses

    def _three_nt_options(self, overcall_suit: str) -> list[str]:
        suit = suit_html(overcall_suit)
        return (
            f"Denies stop in {suit}, denies 4+ card major",
            f"Promises stop in {suit}, denies 4+ card major",
            f"Denies stop in {suit}, promises 4+ card major",
            f"Promises stop in {suit}, promises 4+ card major",
            f"Invitational in {suit} (promises 6+ cards)",
            f"To play in {suit}",
            f"Asking for stop in {suit}",
        )


class OpenersInterpretationAfterOneNt(OpenersInterpretation):
    def __init__(self):
        super().__init__(AFTER_1NT)
        self.auction = [
            "1NT",
            self.response.opponents_bid,
            self.response.response,
        ]
        self.dealer = "N"
        self.challenge = self._build_challenge().challenge


class OpenersInterpretationAfterWeakTwo(OpenersInterpretation):
    def __init__(self):
        super().__init__(AFTER_WEAK_2)
        self.auction = [
            self.response.opponents_bid,
            "D",
            "P",
            self.response.response,
        ]
        self.dealer = "W"
        self.challenge = self._build_challenge().challenge


QUESTION_CLASSES: list[tuple[type, int]] = [
    (ResponseToOneNt, 1),
    (ResponseToWeakTwoDoubled, 3),
    (OpenersInterpretationAfterOneNt, 3),
    (OpenersInterpretationAfterWeakTwo, 3),
]


challenge = NextQuestion(QUESTION_CLASSES).challenge
