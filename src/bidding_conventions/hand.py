from bfgdealer.dealer_bidding import Dealer as BiddingDealer
from bfgdealer.dealer_solo import Dealer as SoloDealer
from bridgeobjects import VULNERABILITY
from bridgeobjects import Hand as HandBase

SUIT_ORDER = ["S", "H", "C", "D"]


class Hand(HandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand_number = 0
        self._sorted_card_names = []
        self._vulnerability = ""
        self.dealer = ""
        self.auction = []

    @property
    def sorted_card_names(self) -> list[str]:
        sorted_hand = Hand.sort_card_list(self.cards, SUIT_ORDER)
        self._sorted_card_names = [card.name for card in sorted_hand]
        return self._sorted_card_names

    @property
    def vulnerability(self) -> str:
        self._vulnerability = VULNERABILITY[self.hand_number % 16]
        return self._vulnerability


def asptro_overcaller_hand(holding: str, points: tuple[int, int]) -> Hand:
    global hand_number
    dealer = BiddingDealer()
    board = dealer.asptro_overcaller(holding, points)
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def opening_one_hand() -> Hand:
    global hand_number
    dealer = SoloDealer()
    stage = dealer.set_hands_list.index("Opening ones")
    board = dealer.get_set_hand([stage], "N")
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.auction = [call.name for call in board.auction.calls]
    hand.hand_number = hand_number
    hand_number += 1
    return hand


# Global hand number used to calulate vulnerability
hand_number = 0
