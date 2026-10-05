import random
import re
from dataclasses import asdict, dataclass, field

from bidding_conventions.constants import (
    RANDOM_MINOR,
    SUIT_MAP,
    SUIT_RE,
)
from bidding_conventions.text import Text

txt = Text()


# VALID_ELEMENTS = {element.value for element in DisplayElements}


@dataclass
class Challenge:
    """One bidding question, as sent to the front end."""

    # auction is a list of bids, where each bid is a string like "1H"
    # or "P" or "X" or "XX" or "cursor"
    theme: str
    title: str = ""
    preamble: str = ""
    question: str = ""
    options: list[str] = field(default_factory=list)
    correct_response: str = ""
    description: str = ""
    hand_cards: list[str] | None = None
    vulnerability: str | None = None
    dealer: str | None = None
    auction: list[str] = field(default_factory=list)
    display_elements: list[str] = field(default_factory=list)
    bid_suppression: list = field(default_factory=list)

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
        return asdict(self) | {
            "subtitle": self._build_subtitle(),
            "preamble": self._build_preamble(),
        }

    def display(self) -> None:
        items = (
            f"preamble: {self._build_preamble()}",
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
