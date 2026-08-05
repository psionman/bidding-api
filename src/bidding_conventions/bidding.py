from bridgeobjects import Card, Suit

from bidding_conventions.hand import Hand


def stoppers_in_bid_suits(hand: Hand, auction: list[str]) -> bool:
    """Return True if hand contains stoppers
    in all opponent's bid suits."""
    return _stoppers_in_bid_suits(hand, auction)


def poor_stoppers_in_bid_suits(hand: Hand, auction: list[str]) -> bool:
    """Return True if hand contains stoppers (including ten)
    in all opponent's bid suits."""
    return _stoppers_in_bid_suits(hand, auction, lowest_card="T")


def _stoppers_in_bid_suits(hand: Hand, auction: list[str], lowest_card="J"):
    """Return True if hand contains stoppers
    in all opponent's bid suits."""
    return all(
        suit_stopper(hand, Suit(bid[1]), lowest_card)
        for bid in auction
        if bid[1] != "N"
    )


def suit_stopper(hand: Hand, suit: Suit, lowest_card: str = "J") -> bool:
    """Return True if the hand contains a stopper in 'suit'."""
    if not suit:
        return False

    suit_holding = hand.suit_holding
    if suit_holding[suit] >= 5:
        return True

    poor_stopper = False
    ace_stopper = Card("A", suit.name) in hand.cards
    king_stopper = (
        Card("K", suit.name) in hand.cards and suit_holding[suit] >= 2
    )
    queen_stopper = (
        Card("Q", suit.name) in hand.cards and suit_holding[suit] >= 3
    )
    jack_stopper = (
        Card("J", suit.name) in hand.cards and suit_holding[suit] >= 4
    )
    if lowest_card == "T":
        poor_stopper = (
            Card("T", suit.name) in hand.cards and suit_holding[suit] >= 4
        )
    return (
        ace_stopper
        or king_stopper
        or queen_stopper
        or jack_stopper
        or poor_stopper
    )
