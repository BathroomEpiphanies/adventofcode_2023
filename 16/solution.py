from __future__ import annotations

import sys

from collections import deque
from enum import Enum


def parse_input(file_handle) -> dict[complex,str]:
    return {x+y*1j:c for y,row in enumerate(l.strip() for l in file_handle.readlines()) for x,c in enumerate(row)}


class DIR(complex, Enum):
    RG = +1+0j
    UP = +0-1j
    LF = -1+0j
    DW = +0+1j


redirect:dict[str,dict[DIR,list[DIR]]] = {
    '\\': {DIR.RG:[DIR.DW], DIR.UP:[DIR.LF], DIR.LF:[DIR.UP], DIR.DW:[DIR.RG]},
    '/':  {DIR.RG:[DIR.UP], DIR.UP:[DIR.RG], DIR.LF:[DIR.DW], DIR.DW:[DIR.LF]},
    '-':  {DIR.RG:[DIR.RG], DIR.UP:[DIR.RG,DIR.LF], DIR.LF:[DIR.LF], DIR.DW:[DIR.RG,DIR.LF]},
    '|':  {DIR.RG:[DIR.DW,DIR.UP], DIR.UP:[DIR.UP], DIR.LF:[DIR.DW,DIR.UP], DIR.DW:[DIR.DW]},
    '.':  {DIR.RG:[DIR.RG], DIR.UP:[DIR.UP], DIR.LF:[DIR.LF], DIR.DW:[DIR.DW]},
}


def energization_from_start(device:dict[complex,str], entry_point:complex, direction:DIR):
    beam = (entry_point, direction)
    visited = set()
    queue = deque( [beam] )
    while queue:
        position,direction = queue.popleft()
        position = position+direction
        if not position in device:
            continue
        directions = [d for d in redirect[device[position]][direction]]
        for direction in directions:
            beam = position,direction
            if beam not in visited:
                queue.append(beam)
                visited.add(beam)
    return len({p for p,_ in visited})


def star1(problem_input:dict[complex,str]) -> int:
    return energization_from_start(problem_input, -1+0j, DIR.RG)


def star2(problem_input:dict[complex,str]) -> int:
    maxx = round(max(p.real for p in problem_input))
    maxy = round(max(p.imag for p in problem_input))
    best = 0
    for x in range(maxx):
        best = max(best, energization_from_start(problem_input, x +         -1j, DIR.DW))
        best = max(best, energization_from_start(problem_input, x + (maxy+1)*1j, DIR.UP))
    for y in range(maxy):
        best = max(best, energization_from_start(problem_input, -1       + y*1j, DIR.RG))
        best = max(best, energization_from_start(problem_input, (maxx+1) + y*1j, DIR.LF))
    return best


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
