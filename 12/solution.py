from __future__ import annotations

from functools import cache


def parse_input(file_handle) -> list[tuple[str,tuple[int,...]]]:
    springs = []
    for line in (l.strip() for l in file_handle.readlines()):
        spring,lengths_ = line.split(' ')
        lengths = tuple(int(n) for n in lengths_.split(','))
        springs.append((spring,lengths))
    return springs


@cache
def fit_lengths_to_spring(spring:str, lengths:tuple[int,...]):
    if not lengths:
        if not any(c=='#' for c in spring):
            return 1
        else:
            return 0
    total = 0
    length = lengths[0]
    for pos,_ in enumerate(spring[:-length]):
        if all(c in {'#','?'} for c in spring[pos:pos+length]) and spring[pos+length] != '#':
            total += fit_lengths_to_spring(spring[pos+length+1:], lengths[1:])
        if spring[pos] == '#':
            break
    return total


def part1(problem_input:list[tuple[str,tuple[int,...]]]) -> int:
    return sum(fit_lengths_to_spring(spring+'.', tuple(lengths)) \
               for spring,lengths in problem_input)


def part2(problem_input:list[tuple[str,tuple[int,...]]]) -> int:
    return sum(fit_lengths_to_spring('?'.join([spring]*5)+'.', lengths*5) \
               for spring,lengths in problem_input)
