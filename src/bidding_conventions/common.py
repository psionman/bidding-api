from bridgeobjects import Hand

from bidding_conventions.constants import HandStrength


def hand_strength(hand: Hand) -> HandStrength:
    if hand.hcp <= 9:
        return HandStrength.WEAK
    if 10 <= hand.hcp <= 11:
        return HandStrength.INTERMEDIATE
    return HandStrength.STRONG
