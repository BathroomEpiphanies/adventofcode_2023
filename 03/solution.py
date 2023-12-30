from __future__ import annotations
from typing import Iterable

import operator
import pprint
import sys

from functools import reduce
from itertools import product


def parse_input(file_handle) -> Machine:
    return Machine([l.strip() for l in file_handle.readlines()])


class Part:
    
    def __init__(self, location:Iterable[complex], value:str) -> None:
        self.location:frozenset[complex] = frozenset(location)
        self.value:int = int(value)
    
    def is_adjecent(self, other:Part) -> bool:
        return any(abs(p-q)<1.42 for p,q in product(self.location, other.location))
        
    def __hash__(self) -> int:
        return hash(self.location)
    
    def __str__(self) -> str:
        return f'{self.value}: {set(self.location)}'
    
    __repr__ = __str__


class Connector(Part):
    
    def __init__(self, location:Iterable[complex], operator:str) -> None:
        self.location:frozenset[complex] = frozenset(location)
        self.operator:str = operator
        self.parts:set[Part] = set()
    
    def __str__(self) -> str:
        return f'{self.operator}: {set(self.location)} -> {str(self.parts)}'


class Machine:
    
    def __init__(self, description:list[str]) -> None:
        self.parts:set[Part] = set()
        self.connectors:set[Connector] = set()
        for y,row in enumerate(description):
            x = 0
            while x<len(row):
                c = row[x]
                if c == '.':
                    x += 1
                elif c in '0123456789':
                    w = x
                    while w<len(row) and row[w] in '0123456789':
                        w += 1
                    self.parts.add( Part((x+y*1j for x in range(x,w)), row[x:w]) )
                    x = w
                else:
                    self.connectors.add( Connector((x+y*1j,), c) )
                    x += 1
        for connector,part in product(self.connectors, self.parts):
            if part.is_adjecent(connector):
                connector.parts.add(part)
    
    def __str__(self) -> str:
        return pprint.pformat(self.parts)+'\n'+pprint.pformat(self.connectors)
    
    def part_sum(self) -> int:
        connected_parts:set[Part] = {p for c in self.connectors for p in c.parts}
        return sum(p.value for p in connected_parts)
    
    def gear_sum(self) -> int:
        sum = 0
        for connector in (c for c in self.connectors if c.operator=='*' and len(c.parts)>=2):
            #print(connector)
            sum += reduce(operator.mul, (p.value for p in connector.parts))
        return sum


def star1(problem_input:Machine) -> int:
    return problem_input.part_sum()


def star2(problem_input:Machine) -> int:
    return problem_input.gear_sum()


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
