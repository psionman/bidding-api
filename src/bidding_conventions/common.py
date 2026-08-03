from bridgeobjects import CALLS, Call, Denomination, Hand

from bidding_conventions.constants import SUIT_MAP, HandStrength


def hand_strength(hand: Hand) -> HandStrength:
    if hand.hcp <= 9:
        return HandStrength.WEAK
    if 10 <= hand.hcp <= 11:
        return HandStrength.INTERMEDIATE
    return HandStrength.STRONG


def bid_options(lowest: str = "1C", highest: str = "7NT"):
    start = CALLS.index(lowest)
    end = CALLS.index(highest)
    selected_calls = CALLS[start:end]
    return [_html_call(call) for call in selected_calls]


def _html_call(call: str) -> str:
    if call[1] == "N":
        return call
    return f"{call[:-1]}{suit_html(call[1])}"


def suit_html(suit_str: str) -> str:
    colour, suit = SUIT_MAP[suit_str.upper()]
    return f'<span class="{colour}-suit">{suit}</span>'


def hand_shape(hand: Hand) -> str:
    spades = f"{hand.spades}S, " if hand.spades else ""
    hearts = f"{hand.hearts}H, " if hand.hearts else ""
    diams = f"{hand.diamonds}D, " if hand.diamonds else ""
    clubs = f"{hand.clubs}C" if hand.clubs else ""
    return f"{spades}{hearts}{diams}{clubs}"


def get_suppressed_calls(calls: list) -> dict:
    if "cursor" in calls:
        calls = calls[:-1]
    call = _get_last_call(calls)

    denoms = []

    for denom in Denomination.SHORT_NAMES:
        denoms.append(denom)
        if denom == call[1:]:
            break

    level = int(call[0])
    if call[1:] == "NT":
        denoms = []
        level += 1

    can_double = _can_double(calls)
    can_redouble = _can_redouble(calls)

    return {
        "level": level,
        "suppress_denoms": denoms,
        "can_double": can_double,
        "can_redouble": can_redouble,
    }


def _get_last_call(calls: list) -> str:
    for call in reversed(calls):
        if Call(call).is_value_call:
            return call
    return ""


def _can_double(calls: list) -> bool:
    if calls and Call(calls[-1]).is_value_call:
        return True
    if (
        len(calls) >= 3
        and Call(calls[-3]).is_value_call
        and Call(calls[-2]).is_pass
        and Call(calls[-1]).is_pass
    ):
        return True
    return False


def _can_redouble(calls: list) -> bool:
    if calls and Call(calls[-1]).is_double:
        return True
    return bool(
        len(calls) >= 3
        and Call(calls[-3]).is_double
        and Call(calls[-2]).is_pass
        and Call(calls[-1]).is_pass
    )
