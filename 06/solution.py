from __future__ import annotations

import re

from math import ceil, floor, sqrt


def parse_input(file_handle) -> tuple[list[int], list[int]]:
    lines = file_handle.readlines()
    durations = [int(n) for n in re.split(r' +', lines[0].strip())[1:]]
    records = [int(n) for n in re.split(r' +', lines[1].strip())[1:]]
    return durations,records


def hold_range_to_win(duration:int, record:int) -> tuple[int,int]:
    _record = record + 0.1
    return ceil(duration/2-sqrt(duration**2//4-_record)), floor(duration/2+sqrt(duration**2//4-_record))


def part1(problem_input:tuple[list[int], list[int]]) -> int:
    durations,records = problem_input
    margin = 1
    for duration,record in zip(durations, records):
        lower,upper = hold_range_to_win(duration, record)
        margin *= (upper-lower+1)
    return margin


def part2(problem_input:tuple[list[int], list[int]]) -> int:
    durations,records = problem_input
    duration = int(''.join(str(t) for t in durations))
    record = int(''.join(str(r) for r in records))
    lower,upper = hold_range_to_win(duration, record)
    return upper-lower+1
