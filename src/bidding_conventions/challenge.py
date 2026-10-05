import random
import re
from enum import Enum

from bidding_conventions.constants import (
    RANDOM_MINOR,
    SUIT_MAP,
    SUIT_RE,
)
from bidding_conventions.text import Text

txt = Text()


class DisplayElements(Enum):
    HAND = "hand"
    AUCTION = "auction"
    PREAMBLE = "preamble"
    BIDDING_BOX = "bidding_box"


class Challenge:
    # auction is a list of bids, where each bid is a string like "1H"
    # or "P" or "X" or "XX" or "cursor"
    def __init__(
        self,
        theme: str,
        title: str = "",
        preamble: str = "",
        question: str = "",
        options: list[str] | None = None,
        correct_response: str = "",
        description: str = "",
        hand_cards: list[str] | None = None,
        vulnerability: str | None = None,
        dealer: str | None = None,
        auction: list[str] | None = None,
        display_elements: list[str] | None = None,
        bid_suppression: list | None = None,
    ) -> None:

        self.theme = theme
        self.title = title
        self.preamble = preamble
        self.question = question
        self.options = options if options else []
        self.correct_response = correct_response
        self.description = description
        self.hand_cards = hand_cards
        self.vulnerability = vulnerability
        self.dealer = dealer
        self.auction = auction or []
        self.display_elements = display_elements or []
        self.bid_suppression = bid_suppression or []

    @property
    def response(self) -> dict:
        for element in self.display_elements:
            if element not in [e.value for e in DisplayElements]:
                raise ValueError(f"Invalid display element: {element}")
        return {
            "theme": self.theme,
            "title": self.title,
            "subtitle": self._build_subtitle(),
            "preamble": self._build_preamble(),
            "question": self.question,
            "options": self.options,
            "correct_response": self.correct_response,
            "description": self.description,
            "hand_cards": self.hand_cards,
            "vulnerability": self.vulnerability,
            "dealer": self.dealer,
            "auction": self.auction,
            "display_elements": self.display_elements,
            "bid_suppression": self.bid_suppression,
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
        return f"{txt.SUB_TITLE_PREFIX} {self.title} {txt.SUB_TITLE_SUFFFIX}"

    def _build_preamble(self) -> str:
        words = self.preamble.split()
        converted = [self._suit_conversion(word) for word in words]
        return " ".join(converted)

    def _build_options(self) -> list:
        delimiter = "-" * 50
        options = delimiter
        for option in self.options:
            options = f"{options}\n{option}"
        options = f"{options}\n{delimiter}"
        return options

    def _suit_conversion(self, text: str) -> str:
        def replace_holding(match):
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
