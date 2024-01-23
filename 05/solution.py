from __future__ import annotations

from dataclasses import dataclass
from more_itertools import chunked


@dataclass
class Interval:
    lower:int
    upper:int
    offset:int
    
    def __lt__(self, other:Interval):
        return self.lower < other.lower


class Map:
    
    def __init__(self, intervals:list[Interval]) -> None:
        self.intervals = sorted(intervals)
    
    def __getitem__(self, key:int) -> int:
        for interval in self.intervals:
            if interval.lower <= key < interval.upper:
                return key+interval.offset
        return key


def parse_input(file_handle) -> tuple[list[int],list[Map]]:
    seeds:list[int] = []
    maps:list[Map] = []
    lines = (l.strip() for l in file_handle.readlines())
    for line in lines:
        if not line:
            continue
        tag,numbers = line.split(':')
        if tag == 'seeds':
            seeds = [int(n) for n in numbers.strip().split(' ')]
        else:
            tag = tag.split(' ')[0]
            intervals = []
            for line in lines:
                if not line:
                    break
                destination, source, length = (int(n) for n in line.strip().split(' '))
                intervals.append(Interval(source,source+length,destination-source))
            maps.append(Map(intervals))
    return seeds,maps


def part1(problem_input:tuple[list[int],list[Map]]) -> int:
    locations = []
    seeds,maps = problem_input
    for seed in seeds:
        for map in maps:
            seed = map[seed]
        locations.append(seed)
    return min(locations)


def part2(problem_input:tuple[list[int],list[Map]]) -> int:
    def find_min_recursively(maps:list[Map], lower:int, upper:int) -> int:
        # Add "guard" intervals, of length 0, to make sure the whole interval is covered.
        # Look at intervals pairwise.
        # Propagate the first (within overall interval)
        # Propagate the interval inbetween the pair
        if not maps:
            return lower
        minimums = []
        intervals = [Interval(lower, lower, 0)] + maps[0].intervals + [Interval(upper, upper, 0)]
        for i1,i2 in zip(intervals[:-1], intervals[1:]):
            lower_ = max(lower, i1.lower)
            upper_ = min(upper, i1.upper)
            if upper_ > lower_:
                minimums.append( find_min_recursively(maps[1:], lower_+i1.offset, upper_+i1.offset) )
            lower_ = max(lower, i1.upper)
            upper_ = min(upper, i2.lower)
            if upper_ > lower_:
                minimums.append( find_min_recursively(maps[1:], lower_, upper_) )
        return min(minimums)
    
    seeds,maps = problem_input
    locations = []
    for start,length in chunked(seeds, 2):
        locations.append( find_min_recursively(maps, start, start+length) )
    return min(locations)
