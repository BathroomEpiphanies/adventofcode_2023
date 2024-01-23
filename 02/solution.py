from __future__ import annotations

import operator

from dataclasses import dataclass
from functools import reduce


def parse_input(file_handle) -> list[list[BallSet]]:
    return [
        [BallSet.from_str(set_) for set_ in line.split(':')[1].split(';')]
        for line in [l.strip() for l in file_handle.readlines()]
    ]


@dataclass
class BallSet:
    
    red:int = 0
    green:int = 0
    blue:int = 0
    
    @staticmethod
    def from_str(pick:str) -> BallSet:
        balls = [b.strip() for b in pick.split(',')]
        _pick = {}
        for ball in balls:
            count,color = ball.split(' ')
            _pick[color] = int(count)
        return BallSet(**_pick)
    
    def __gt__(self, other:BallSet) -> bool:
        return self.red > other.red or \
               self.green > other.green or \
               self.blue > other.blue
    
    def __or__(self, other:BallSet) -> BallSet:
        return BallSet(
            max(self.red, other.red),
            max(self.green, other.green),
            max(self.blue, other.blue)
        )
    
    def __abs__(self) -> int:
        return self.red * self.green * self.blue


def part1(problem_input:list[list[BallSet]]) -> int:
    ball_counts = BallSet(red=12, green=13, blue=14)
    return sum(id_ for id_,game in enumerate(problem_input, 1)
               if not any(pick>ball_counts for pick in game))


def part2(problem_input:list[list[BallSet]]) -> int:
    return sum(abs(reduce(operator.or_, game)) for game in problem_input)
