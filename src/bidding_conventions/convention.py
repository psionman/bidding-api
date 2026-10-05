# bidding_conventions/convention.py

from __future__ import annotations

import dataclasses
import hashlib
import random
from abc import ABC
from collections.abc import Sequence

from bidding_conventions.challenge import Challenge
from bidding_conventions.descriptions import get_description
from bidding_conventions.text import Text

# Maximum attempts to find a class/answer that differs from the previous
# question before giving up and accepting whatever was last generated.
MAX_REPEAT_AVOIDANCE_ATTEMPTS = 15


"""
Convention tree structure:
- id (str): A URL-safe slug uniquely identifying the convention.
- name (str): The human-readable name of the convention.
- children (list): A list of child convention nodes in the same
  structure, or an empty list if the node is a leaf.
- any (bool): Whether any of the children are selectable.
"""
CONVENTION_TREE = [
    # Defence of 1NT
    {
        "id": "defence-of-1nt",
        "name": "Defence of 1NT",
        "children": [
            {"id": "asptro", "name": "Asptro", "children": []},
            {"id": "multi-landy", "name": "Multi-Landy", "children": []},
        ],
    },
    # Miscellaneous
    # {"id": "ghestem", "name": "Ghestem", "children": []},
    {"id": "lebensohl", "name": "Lebensohl", "children": []},
    # {"id": "puppet-stayman", "name": "Puppet Stayman", "children": []},
    # 5 Card Majors
    {
        "id": "five-card-majors",
        "name": "5 Card Majors",
        "children": [
            {
                "id": "five-cm-opener",
                "name": "Opening bids",
                "children": [],
            },
            {
                "id": "five-cm-responder-bid-one",
                "name": "Responder's bid",
                "children": [],
            },
            {
                "id": "2-way-checkback",
                "name": "2-way checkback",
                "children": [],
            },
        ],
        "any": True,
    },
]


@dataclasses.dataclass
class Response:
    overcall: str
    response: str
    options: list[str]
    correct_response_index: int
    hash_id: str = dataclasses.field(init=False, repr=False)

    def __post_init__(self) -> None:
        payload = "|".join(
            [
                self.overcall,
                self.response,
                *self.options,
                str(self.correct_response_index),
            ]
        )
        self.hash_id = hashlib.sha256(payload.encode()).hexdigest()


class Convention(ABC):
    """Base for a bidding-convention question generator."""

    title: str
    description_file: str  # e.g. "lebensohl.html"
    # Optional: weighted list of (QuestionGenerator, weight)
    question_classes: Sequence[tuple[type, int]] = ()

    def __init__(self) -> None:
        self.txt = Text()
        self.description = get_description(self.description_file)
        # anti-repeat state lives on the instance
        self._last_class = None
        self._last_bid = None
        self._last_response = None

    @property
    def convention_title(self) -> str:
        return self.title

    @property
    def convention_description(self) -> str:
        return self.description

    def challenge(self) -> Challenge:
        """Default implementation: weighted pick with simple anti-repeat."""
        if not self.question_classes:
            raise NotImplementedError("No question_classes defined")

        classes, weights = zip(*self.question_classes, strict=True)
        chosen = None
        q = None
        for _ in range(15):  # MAX_REPEAT_AVOIDANCE_ATTEMPTS
            chosen = self._pick_class(classes, weights)
            q = chosen().question
            if q.correct_response != self._last_bid:
                break

        self._last_class = chosen
        self._last_bid = q.correct_response
        return q

    def _pick_class(self, classes, weights):
        if len(classes) == 1:
            return classes[0]
        while True:
            chosen = random.choices(classes, weights=weights, k=1)[0]
            if chosen is not self._last_class:
                return chosen


class NextQuestion:
    def __init__(self, question_classes: list[tuple[type, int]]):
        self.question_classes = question_classes

    def challenge(self) -> Challenge:
        """Build a new question avoiding repeated classes and correct bids."""
        global last_class, last_bid

        classes, weights = zip(*self.question_classes, strict=True)

        for _ in range(MAX_REPEAT_AVOIDANCE_ATTEMPTS):
            chosen_class = self._pick_class(classes, weights)

            # Avoid the same class as the previous question.
            if chosen_class is last_class:
                continue

            q = chosen_class().challenge

            # Avoid the same correct-response bid as the previous question.
            if q.correct_response == last_bid:
                continue

            last_class = chosen_class
            last_bid = q.correct_response
            return q

        # Fallback if avoidance wasn't possible.
        chosen_class = self._pick_class(classes, weights)
        q = chosen_class().challenge

        last_class = chosen_class
        last_bid = q.correct_response
        return q

    def _pick_class(
        self, classes: tuple[type, ...], weights: tuple[int, ...]
    ) -> type:
        """Pick a weighted-random class, avoiding a repeat of last_class
        where more than one class is available."""
        if len(classes) == 1:
            return classes[0]
        while True:
            chosen = random.choices(classes, weights=weights, k=1)[0]
            if chosen is not last_class:
                return chosen


last_response = None
last_class = None
last_bid = None
