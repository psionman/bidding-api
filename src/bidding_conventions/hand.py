from bfgdealer.dealer_bidding import Dealer as BiddingDealer
from bfgdealer.dealer_duo import Dealer as DuoDealer
from bfgdealer.dealer_solo import Dealer as SoloDealer
from bridgeobjects import SEATS, SUITS, VULNERABILITY
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

    @property
    def losers(self) -> int:
        return self._get_loser_count()

    def _get_loser_count(self) -> int:
        losers = 0
        for suit in SUITS:
            card_points = [
                card.high_card_points for card in self.cards_by_suit[suit]
            ]
            hcps = sorted(card_points, reverse=True)
            if len(hcps) > 0 and hcps[0] == 2:
                losers += min(len(hcps), 3)
                continue
            for rank in hcps[:3]:
                if rank <= 1:
                    losers += 1
                pass
        return losers


def one_nt_openers_hand(dealer: str = "N") -> Hand:
    global hand_number
    dealer = DuoDealer()
    stage = dealer.set_hands_names.index("Weak NT")
    board = dealer.get_set_hand(stage)
    hand = board.hands["S"]
    board.rotate_dealer_to("S")
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.auction = [call.name for call in board.auction.calls]
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def weak_two_openers_hand(dealer: str = "N") -> Hand:
    global hand_number
    dealer = DuoDealer()
    stage = dealer.set_hands_names.index("Weak NT")
    board = dealer.get_set_hand(stage)
    hand = board.hands["S"]
    board.rotate_dealer_to("S")
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.auction = [call.name for call in board.auction.calls]
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def one_nt_overcaller_hand(holding: str, points: tuple[int, int]) -> Hand:
    """
    Create a hand for overcaller after 1NT opener.

    Args:
        holding: The holding of the hand (e.g., {'C': 5, 'D': 5})
        points: The HCP  points range (e.g., (9, 15))

    Returns:
        Hand: The hand with the specified holding and points

    It requires that opener (W) bids 1NT, i.e. is balanced and has 12-14 points;
    The next seat (N) must have the relevant points and shape.
    """
    global hand_number
    dealer = BiddingDealer()
    board = dealer.one_nt_overcaller(holding, points)
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def one_nt_advancers_hand(
    holding: dict[str, int], points: tuple[int, int]
) -> Hand:
    global hand_number
    dealer = BiddingDealer()
    board = dealer.one_nt_overcaller(holding, points)
    board.rotate_dealer_to("E")
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.hand_number = hand_number
    hand_number += 1
    return hand


def one_nt_lebensohl_hand(
    holding: dict[str, int], points: tuple[int, int]
) -> Hand:
    global hand_number
    dealer = BiddingDealer()
    board = dealer.one_nt_overcaller(holding, points)
    board.rotate_dealer_to("S")
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


def weak_two_opener() -> Hand:
    global hand_number
    dealer = SoloDealer()
    while True:
        board = dealer.response_to_weak_two_board(0)
        board.rotate_dealer_to("E")
        if board.hands["S"].hcp >= 12:
            break
    hand = board.hands["N"]
    hand.__class__ = Hand
    hand.dealer = board.dealer
    hand.hand_number = hand_number
    hand_number += 1
    openers_hand = board.hands["E"]
    suit = openers_hand.longest_suit
    hand.auction = [f"2{suit.name}", "D", "P", "cursor"]
    return hand


def print_hands(board):
    print(f"Dealer: {board.dealer} {board.auction}")
    for seat in SEATS:
        hand = board.hands[seat]
        hand.__class__ = Hand
        print(f"{seat}: {hand.hcp:>2} {hand.shape} {hand.sorted_card_names}")
    print("_" * 80)


RANK_ORDER = "AKQJT98765432"
SUIT_ORDER = "SHDC"
SUIT_SYMBOLS = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}

RED_SUITS = {"H", "D"}

RED = "\033[31m"
RESET = "\033[0m"


# def __repr__(self) -> str:
def display_hand(hand):
    lines = []
    for suit in SUIT_ORDER:
        ranks = [card.name[0] for card in hand.cards if card.name[1] == suit]
        ranks.sort(key=RANK_ORDER.index)
        ranks_str = " ".join(ranks) if ranks else "—"
        symbol = SUIT_SYMBOLS[suit]
        line = f"{symbol} {ranks_str}"
        if suit in RED_SUITS:
            line = f"{RED}{line}{RESET}"
        lines.append(line)
    print("\n".join(lines))
    print("-" * 20)
    print(f"{hand.shape}, {hand.hcp}")
    print("-" * 20)


# Global hand number used to calculate vulnerability
hand_number = 0
