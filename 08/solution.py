from __future__ import annotations

from itertools import cycle
from math import lcm


def parse_input(file_handle) -> tuple[str,dict[str,tuple[str,str]]]:
    lines = [l.strip() for l in file_handle.readlines()]
    route = lines[0]
    maps = {}
    for line in lines[2:]:
        pos,leftright = line.split(' = ')
        left,right = leftright[1:-1].split(', ')
        maps[pos] = (left,right)
    return route,maps


def find_distance(position, route, maps):
    for distance,step in enumerate(cycle(route)):
        if position[-1] == 'Z':
            break
        position = maps[position][0] if step=='L' else maps[position][1]
    return distance


def part1(problem_input) -> int:
    route,maps = problem_input
    return find_distance('AAA', route, maps)


def part2(problem_input) -> int:
    route,maps = problem_input
    positions = {p for p in maps if p[-1] == 'A'}
    cycles = {find_distance(p, route, maps) for p in positions}
    return lcm(*cycles)
