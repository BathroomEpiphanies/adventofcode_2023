from __future__ import annotations

import enum

from collections import Counter


def parse_input(file_handle) -> list[Hand]:
    hands = []
    for line in file_handle.readlines():
        cards,bid = line.strip().split(' ')
        hands.append(Hand(cards,int(bid)))
    return hands


class Card(int, enum.Enum):
    
    _1 = enum.auto()
    _2 = enum.auto()
    _3 = enum.auto()
    _4 = enum.auto()
    _5 = enum.auto()
    _6 = enum.auto()
    _7 = enum.auto()
    _8 = enum.auto()
    _9 = enum.auto()
    _T = enum.auto()
    _J = enum.auto()
    _Q = enum.auto()
    _K = enum.auto()
    _A = enum.auto()


class HandType(int, enum.Enum):
    
    HighCard = enum.auto()
    OnePair = enum.auto()
    TwoPair = enum.auto()
    ThreeOfKind = enum.auto()
    FullHouse = enum.auto()
    FourOfKind = enum.auto()
    FiveOfKind = enum.auto()
    
    @staticmethod
    def parse(hand:Hand) -> HandType:
        counter = Counter(hand.cards)
        card_counts = sorted((count,card) for card,count in counter.items())
        if Card._1 in counter:
            count = counter[Card._1]
            _,max_card = card_counts[-1]
            if max_card is Card._1 and len(counter)>1:
                _,max_card = card_counts[-2]
            counter[max_card] += count
            counter[Card._1] -= count
            card_counts = sorted((count,card) for card,count in counter.items())
        if card_counts[-1][0] == 5:
            hand_type = HandType.FiveOfKind
        elif card_counts[-1][0] == 4:
            hand_type = HandType.FourOfKind
        elif card_counts[-1][0] == 3:
            if card_counts[-2][0] == 2:
                hand_type = HandType.FullHouse
            else:
                hand_type = HandType.ThreeOfKind
        elif card_counts[-1][0] == 3:
            if card_counts[-2][0] == 2:
                hand_type = HandType.FullHouse
            else:
                hand_type = HandType.ThreeOfKind
        elif card_counts[-1][0] == 2:
            if card_counts[-2][0] == 2:
                hand_type = HandType.TwoPair
            else:
                hand_type = HandType.OnePair
        else:
            hand_type = HandType.HighCard
        return hand_type


class Hand:
    
    def __init__(self, cards:str, bid:int):
        self.cards = [Card[f'_{c}'] for c in cards]
        self.bid = bid
        self.type = HandType.parse(self)
    
    def __str__(self) -> str:
        return f'{self.type}, {" ".join(c.name[1] for c in self.cards)}: {self.bid}'
    
    def __lt__(self, other:Hand):
        return (self.type, tuple(self.cards)) < (other.type, tuple(other.cards))
    


def part1(problem_input:list[Hand]) -> int:
    return sum(r*h.bid for r,h in enumerate(sorted(problem_input), 1))


def part2(problem_input:list[Hand]) -> int:
    for hand in problem_input:
        hand.cards = [Card._1 if c is Card._J else c for c in hand.cards]
    for hand in problem_input:
        hand.type = HandType.parse(hand)
    return sum(r*h.bid for r,h in enumerate(sorted(problem_input), 1))
