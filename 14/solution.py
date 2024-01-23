from __future__ import annotations
from typing import Any


def parse_input(file_handle) -> list[str]:
    return [l.strip() for l in file_handle.readlines()]


def transpose_string_matrix(matrix:list[str]) -> list[str]:
    return [''.join(r) for r in zip(*matrix)]


def tilt_rocks_left(rocks:list[str], reverse=False) -> list[str]:
    return [
        '#'.join(''.join(c for c in sorted(p, reverse=not reverse)) for p in row.split('#')) \
        for row in rocks
    ]


def do_tilt_rotation(rocks:list[str]) -> list[str]:
    rocks = transpose_string_matrix(rocks)
    rocks = tilt_rocks_left(rocks)
    rocks = transpose_string_matrix(rocks)
    rocks = tilt_rocks_left(rocks)
    rocks = transpose_string_matrix(rocks)
    rocks = tilt_rocks_left(rocks, reverse=True)
    rocks = transpose_string_matrix(rocks)
    rocks = tilt_rocks_left(rocks, reverse=True)
    return rocks


def part1(problem_input:list[str]) -> int:
    rocks = transpose_string_matrix(problem_input)
    rocks = tilt_rocks_left(rocks)
    rocks = transpose_string_matrix(rocks)
    return sum(r*row.count('O') for r,row in enumerate(reversed(rocks), 1))


def part2(problem_input:list[str]) -> int:
    rocks = problem_input
    configurations:dict[str,int] = {}
    
    remaining_cycles = 1_000_000_000
    while remaining_cycles > 0:
        rocks = do_tilt_rotation(rocks)
        remaining_cycles -= 1
        key = ''.join(rocks)
        if key in configurations:
            cycle_length = configurations[key] - remaining_cycles
            remaining_cycles = remaining_cycles % cycle_length
        configurations[key] = remaining_cycles
    return sum(r*row.count('O') for r,row in enumerate(reversed(rocks), 1))
