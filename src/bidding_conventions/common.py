from bridgeobjects import CALLS, Hand

from bidding_conventions.constants import SUIT_MAP, HandStrength


def hand_strength(hand: Hand) -> HandStrength:
    if hand.hcp <= 9:
        return HandStrength.WEAK
    if 10 <= hand.hcp <= 11:
        return HandStrength.INTERMEDIATE
    return HandStrength.STRONG


def suit_html(suit_str: str) -> str:
    colour, suit = SUIT_MAP[suit_str.upper()]
    return f'<span class="{colour}-suit">{suit}</span>'


def bid_options(lowest: str = "1C", highest: str = "7NT"):
    start = CALLS.index(lowest)
    end = CALLS.index(highest)
    selected_calls = CALLS[start:end]
    return [_html_call(call) for call in selected_calls]


def _html_call(call: str) -> str:
    if call[1] == "N":
        return call
    return f"{call[:-1]}{suit_html(call[1])}"


def hand_shape(hand: Hand) -> str:
    spades = f"{hand.spades}S, " if hand.spades else ""
    hearts = f"{hand.hearts}H, " if hand.hearts else ""
    diams = f"{hand.diams}D, " if hand.diams else ""
    clubs = f"{hand.clubs}C" if hand.clubs else ""
    return f"{spades}{hearts}{diams}{clubs}"
