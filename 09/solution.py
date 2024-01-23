from __future__ import annotations

from copy import copy


def parse_input(file_handle) -> list[list[int]]:
    return [[int(n) for n in l.strip().split(' ')] for l in file_handle.readlines()]


def extrapolate_sequence(sequence:list[int]):
    differences = [copy(sequence)]
    while not all(n==0 for n in differences[-1]):
        differences.append([b-a for a,b in zip(differences[-1][:-1], differences[-1][1:])])
    for diff1,diff2 in zip(reversed(differences[:-1]),reversed(differences[1:])):
        diff1.append(diff1[-1]+diff2[-1])
    for diff1,diff2 in zip(reversed(differences[:-1]),reversed(differences[1:])):
        diff1.insert(0, diff1[0]-diff2[0])
    return differences[0]


def part1(problem_input:list[list[int]]) -> int:
    #print(problem_input)
    return sum(extrapolate_sequence(s)[-1] for s in problem_input)


def part2(problem_input:list[list[int]]) -> int:
    return sum(extrapolate_sequence(s)[0] for s in problem_input)
