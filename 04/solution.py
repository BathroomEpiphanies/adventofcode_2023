from __future__ import annotations

import functools


def parse_input(file_handle) -> list[Card]:
    return [Card.from_string(l.strip()) for l in file_handle.readlines()]


class Card:
    
    def __init__(self, card_id:int, numbers:set[int], winning:set[int]) -> None:
        self.card_id = card_id
        self.numbers = numbers
        self.winning = winning
        self.matches = len(self.numbers & self.winning)
    
    @staticmethod
    def from_string(description:str) -> Card:
        _card_id,tmp = description.split(':')
        card_id = int(_card_id.split(' ')[-1])
        number_list,winning_list = tmp.split('|')
        numbers = {int(n) for n in (n for n in number_list.split(' ') if n)}
        winning = {int(n) for n in (n for n in winning_list.split(' ') if n)}
        return Card(card_id, numbers, winning)
    
    def point_value(self) -> int:
        return 2**(self.matches-1) if self.matches>0 else 0
    
    def __str__(self):
        return f'Card {self.card_id:2d}: {" ".join(f"{n:2d}" for n in self.numbers)} | {" ".join(f"{n:2d}" for n in self.winning)}'
    
    __repr__ = __str__


def part1(problem_input:list[Card]) -> int:
    return sum(c.point_value() for c in problem_input)


def part2(problem_input:list[Card]) -> int:
    @functools.cache
    def card_return(pos:int) -> int:
        matches = problem_input[pos].matches
        return matches + sum(card_return(i) for i in range(pos+1,pos+matches+1))
    return sum(1+card_return(pos) for pos,_ in enumerate(problem_input))
