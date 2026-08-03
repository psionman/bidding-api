from enum import Enum, auto

SUIT_MAP = {
    "S": ("black", "&spades;"),
    "H": ("red", "&hearts;"),
    "D": ("red", "&diams;"),
    "C": ("black", "&clubs;"),
}


SUIT_RE = r"[1-7][SHDCshdc]|no\s[SHDCshdc]"

SUB_TITLE_PREFIX = "Practice bidding with the"
SUB_TITLE_SUFFFIX = "convention"

WHAT_IS_YOUR_BID = "You are sitting in the N seat; what is your bid?"
PARTNERS_HOLDING = "What is partner's holding?"

OPENER_OPENS_1NT = "Opener has bid 1NT"
PARTNERS_OVERCALL = "and partner bids"
YOUR_HOLDING = "you hold"
POINTS = "points"

RANDOM_MINOR = "random_minor"
RANDOM_MAJOR = "random_major"


class HandStrength(Enum):
    WEAK = auto()
    INTERMEDIATE = auto()
    STRONG = auto()
