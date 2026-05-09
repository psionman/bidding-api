import random
import re

from bidding_conventions.constants import (
    RANDOM_MINOR,
    SUB_TITLE_PREFIX,
    SUB_TITLE_SUFFFIX,
    SUIT_MAP,
    SUIT_RE,
)


class Question:
    def __init__(
        self,
        title: str,
        preamble: str,
        question: str,
        options: list[str],
        correct_response: str,
        description: str,
    ) -> None:
        self.title = title
        self.preamble = preamble
        self.question = question
        self.options = options
        self.correct_response = correct_response
        self.description = description
        # self.display()

    @property
    def response(self) -> dict:
        return {
            "title": self.title,
            "subtitle": self._build_subtitle(),
            "preamble": self._build_preamble(),
            "question": self.question,
            "options": self._build_options(),
            "correct_response": self.correct_response,
            "description": self.description,
        }

    def display(self) -> None:
        print(
            # f"title: {self.title}",
            # f"subtitle: {self._build_subtitle()}",
            f"preamble: {self._build_preamble()}",
            # f"question: {self.question}",
            f"options: {self._build_options()}",
            f"correct_response: {self.correct_response}",
            # f"description: {self.description}"
        )

    def _build_subtitle(self) -> str:
        return f"{SUB_TITLE_PREFIX} {self.title} {SUB_TITLE_SUFFFIX}"

    def _build_preamble(self) -> str:
        words = self.preamble.split()
        converted = [self._suit_conversion(word) for word in words]
        return " ".join(converted)

    def _build_options(self) -> list:
        # return [self._suit_conversion(option) for option in self.options]
        return self.options

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
