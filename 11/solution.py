from __future__ import annotations

import sys

from itertools import combinations
from typing import NamedTuple


def parse_input(file_handle) -> Universe:
    return Universe.from_string([l.strip() for l in file_handle.readlines()])


class Galaxy(NamedTuple):
    x:int
    y:int


class Universe:
    
    def __init__(self, galaxies) -> None:
        self.galaxies:set[Galaxy] = galaxies
        self.populated_xs = {g.x for g in galaxies}
        self.populated_ys = {g.y for g in galaxies}
    
    @staticmethod
    def from_string(description:list[str]) -> Universe:
        return Universe({Galaxy(x,y) for y,row in enumerate(description) for x,g in enumerate(row) if g=='#'})
    
    def distances_sum(self, expansion:int) -> int:
        distances_sum = 0
        for g1,g2 in combinations(self.galaxies, 2):
            empty_xs = set(range(g1.x, g2.x, 1 if g2.x>g1.x else -1)) - self.populated_xs
            empty_ys = set(range(g1.y, g2.y, 1 if g2.y>g1.y else -1)) - self.populated_ys
            distance = abs(g2.x-g1.x) + abs(g2.y-g1.y) + len(empty_xs)*(expansion-1) + len(empty_ys)*(expansion-1)
            distances_sum += distance
        return distances_sum


def star1(problem_input:Universe) -> int:
    return problem_input.distances_sum(expansion=2)


def star2(problem_input:Universe) -> int:
    return problem_input.distances_sum(expansion=1_000_000)


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
