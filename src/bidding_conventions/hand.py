from bfgdealer.dealer_bidding import Dealer as BiddingDealer
from bfgdealer.dealer_solo import Dealer as SoloDealer

# from bfgdealer.dealer_duo import Dealer as DuoDealer
from bridgeobjects import SEATS, VULNERABILITY
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
    """
    Create a hand for ASPTRO overcaller convention.

    Args:
        holding: The holding of the hand (e.g., "A K Q J 10 9 8 7 6 5 4 3 2")
        points: The HCP and distribution points (e.g., (10, 5))

    Returns:
        Hand: The hand with the specified holding and points

    It requires that W bids 1NT, i.e. is balanced and has 12-14 points
    N must have 9-16 points nad be ither 2 suited or have a 6+ card suit
    """
    global hand_number
    dealer = BiddingDealer()
    board = dealer.asptro_overcaller(holding, points)
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def asptro_advancers_hand(holding: str, points: tuple[int, int]) -> Hand:
    global hand_number
    dealer = BiddingDealer()
    board = dealer.asptro_overcaller(holding, points)
    board.rotate_dealer_to("E")
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def opening_one_hand() -> Hand:
    global hand_number
    dealer = SoloDealer()
    stage = dealer.set_hands_names.index("Opening ones")
    board = dealer.get_set_hand(stage)
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.auction = [call.name for call in board.auction.calls]
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def print_hands(board):
    print(f"Dealer: {board.dealer} {board.auction}")
    for seat in SEATS:
        hand = board.hands[seat]
        hand.__class__ = Hand
        print(f"{seat}: {hand.hcp:>2} {hand.shape} {hand.sorted_card_names}")
    print("_" * 80)


# Global hand number used to calulate vulnerability
hand_number = 0
