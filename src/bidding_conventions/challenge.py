import dataclasses
import random
import re

from bidding_conventions.constants import (
    RANDOM_MINOR,
    SUIT_MAP,
    SUIT_RE,
)
from bidding_conventions.text import Text

txt = Text()


# VALID_ELEMENTS = {element.value for element in DisplayElements}


@dataclasses.dataclass
class Challenge:
    """One bidding question, as sent to the front end."""

    # auction is a list of bids, where each bid is a string like "1H"
    # or "P" or "X" or "XX" or "cursor"
    theme: str
    title: str = ""
    preamble: str = ""
    question: str = ""
    options: list[str] = dataclasses.field(default_factory=list)
    correct_response: str = ""
    description: str = ""
    hand_cards: list[str] | None = None
    vulnerability: str | None = None
    dealer: str | None = None
    auction: list[str] = dataclasses.field(default_factory=list)
    display_elements: list[str] = dataclasses.field(default_factory=list)
    bid_suppression: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.hand_cards is None:
            self.hand_cards = []
        if self.options is None:
            self.options = []

    @property
    def response(self) -> dict:
        # for element in self.display_elements:
        #     if element not in VALID_ELEMENTS:
        #         raise ValueError(f"Invalid display element: {element}")
        return dataclasses.asdict(self) | {
            "subtitle": self._build_subtitle(),
            "preamble": self._build_preamble(),
        }

    def display(self) -> None:
        items = (
            f"question: {self.question}",
            f"auction: {self.auction}",
            f"options: {self._build_options()}",
            f"correct_response: {self.correct_response}",
            f"hand_cards: {self.hand_cards}",
        )
        for item in items:
            print(item)
        print("*" * 50)
        print("")

    def _build_subtitle(self) -> str:
        return f"{txt.SUB_TITLE_PREFIX} {self.title} {txt.SUB_TITLE_SUFFIX}"

    def _build_preamble(self) -> str:
        words = self.preamble.split()
        converted = [self._suit_conversion(word) for word in words]
        return " ".join(converted)

    def _build_options(self) -> str:
        delimiter = "-" * 50
        options = delimiter
        for option in self.options:
            options = f"{options}\n{option}"
        options = f"{options}\n{delimiter}"
        return options

    @staticmethod
    def _suit_conversion(text: str) -> str:
        def replace_holding(match) -> str:
            s = match.group()
            if s[1] in (" ", "\t"):
                # "no H" style — suit is last character
                colour, suit = SUIT_MAP[s[-1].upper()]
                return f'{s[:-1]}<span class="{colour}-suit">{suit}</span>'
            else:
                # "3H" style
                colour, suit = SUIT_MAP[s[1].upper()]
                return (
                    f'{s[0]}<span class="{colour}-suit">{suit}</span>{s[2:]}'
                )

        if re.match(SUIT_RE, text):
            return re.sub(SUIT_RE, replace_holding, text)

        match text.upper():
            case "D":
                return "Double"
            case "X":
                return "Double"
            case "P":
                return "Pass"
        return text


def random_minor_suit(text) -> str:
    if RANDOM_MINOR not in text:
        return text
    suit = random.choice(["C", "D"])
    return text.replace(RANDOM_MINOR, suit)


# @dataclasses.dataclass
# class Response:
#     opponents_bid: str
#     response: str
#     options: list[str]
#     correct_response_index: int
#     hash_id: str = dataclasses.field(init=False, repr=False)

#     def __post_init__(self) -> None:
#         payload = "|".join(
#             [
#                 self.opponents_bid,
#                 self.response,
#                 *self.options,
#                 str(self.correct_response_index),
#             ]
#         )
#         self.hash_id = hashlib.sha256(payload.encode()).hexdigest()


# class InterpretationQuestion:
#     def __init__(
#         self,
#         response: Response,
#         auction: list[str],
#         dealer: str,
#         vulnerability,
#     ):
#         self.response = response
#         self.auction = auction
#         self.dealer = dealer
#         self.vulnerability = vulnerability

#     @property
#     def challenge(self) -> Challenge:
#         correct_response = self.response.options[
#             self.response.correct_response_index
#         ]

#         return Challenge(
#             theme=CONVENTION_THEME,
#             description=CONVENTION_DESCRIPTION,
#             question=txt.WHAT_DOES_PARTNERS_BID_MEAN,
#             options=self.response.options,
#             correct_response=correct_response,
#             display_elements=["auction"],
#             auction=self.auction,
#             dealer=self.dealer,
#             vulnerability=self.vulnerability,
#         )


def randomize_reponses(
    options: list[str], correct_response_index: int = 0
) -> tuple[list[str], int]:
    correct_option = options[correct_response_index]
    shuffled_options = random.sample(options, k=len(options))
    correct_index = shuffled_options.index(correct_option)
    return shuffled_options, correct_index
