from __future__ import annotations

from collections import deque
from enum import Enum


def parse_input(file_handle) -> tuple[int,complex,dict[complex,str]]:
    grounds = {x+y*1j:g for y,row in enumerate(l.strip() for l in file_handle.readlines()) for x,g in enumerate(row)}
    for start,ground in grounds.items():
        if ground=='S':
            grounds[start] = '.'
            break
    return 6 if len(grounds)<256 else 64, start, grounds


class D(complex, Enum):
    R = +1+0j
    U = +0-1j
    L = -1+0j
    D = +0+1j


def part1(problem_input:tuple[int,complex,dict[complex,str]]) -> int:
    steps_target,start_position,grounds = problem_input
    reachable_in_even_steps = {start_position}
    visited = set()
    queue = deque([(0,start_position)])
    while queue:
        current_step,current_position = queue.popleft()
        for d in D:
            next_position = current_position+d
            next_step = current_step+1
            if next_step > steps_target:
                continue
            if next_position not in grounds or grounds[next_position] != '.':
                continue
            elif next_position not in visited:
                if next_step%2 == 0:
                    reachable_in_even_steps.add(next_position)
                visited.add(next_position)
                queue.append( (next_step,next_position) )
    return len(reachable_in_even_steps)


def part2(problem_input:tuple[int,complex,dict[complex,str]]) -> int:
    """
    The input consists of two diamond shapes, or discs with manhattan distance
    radius 131. There are enough free paths to ensure that all positions that
    are not completely walled off are also reachable in 131 steps.
    
    ......o
    ...x...
    ..xxx..
    .xxSxx.
    ..xxx..
    ...x..o
    o....oo
    
    ......o......o......o......o......o 
    ...x......x......x......x......x...
    ..xxx....xxx....xxx....xxx....xxx.. 
    .xxxxx..xxxxx..xxxxx..xxxxx..xxxxx.
    ..xxx....xxx....xxx....xxx....xxx.. 
    ...x..o...x..o...x..o...x..o...x..o
    o....ooo....ooo....ooo....ooo....oo 
    ......o......o......o......o......o
    ...x......x......x......x......x... 
    ..xxx....xxx....xxx....xxx....xxx..
    .xxxxx..xxxxx..xxxxx..xxxxx..xxxxx. 
    ..xxx....xxx....xxx....xxx....xxx..
    ...x..o...x..o...x..o...x..o...x..o 
    o....ooo....ooo....ooo....ooo....oo
    ......o......o......o......o......o 
    ...x......x......x......x......x...
    ..xxx....xxx....xxx....xxx....xxx.. 
    .xxxxx..xxxxx..xxSxx..xxxxx..xxxxx.
    ..xxx....xxx....xxx....xxx....xxx.. 
    ...x..o...x..o...x..o...x..o...x..o
    o....ooo....ooo....ooo....ooo....oo 
    ......o......o......o......o......o
    ...x......x......x......x......x... 
    ..xxx....xxx....xxx....xxx....xxx..
    .xxxxx..xxxxx..xxxxx..xxxxx..xxxxx. 
    ..xxx....xxx....xxx....xxx....xxx..
    ...x..o...x..o...x..o...x..o...x..o 
    o....ooo....ooo....ooo....ooo....oo
    ......o......o......o......o......o 
    ...x......x......x......x......x...
    ..xxx....xxx....xxx....xxx....xxx.. 
    .xxxxx..xxxxx..xxxxx..xxxxx..xxxxx.
    ..xxx....xxx....xxx....xxx....xxx.. 
    ...x..o...x..o...x..o...x..o...x..o
    .....ooo....ooo....ooo....ooo....oo
    
    Each increment of 131 to the target number of steps adds another ring of
    reachable diamond shapes. Evey other ring of diamonds have similar
    structures. Both odd and even rings increase with, the same, fixed number of
    reachable positions.
    
    Calculate how number of reachable steps increase with increasing number of
    rings. Calculate the number of reachable steps in the n'th ring by adding
    the difference between the (n-2)'th and (n-4)'th ring to the (n-2)'th ring.
    """
    
    steps_target,start_position,grounds = problem_input
    mod_x = round(max(p.real for p in grounds))+1
    mod_y = round(max(p.imag for p in grounds))+1
    
    reachable_in_odd_steps = set()
    discarded = set([(0,start_position)])
    visited = set()
    def find_reachable_in_steps(steps_target):
        queue = deque(discarded)
        while queue:
            item = queue.popleft()
            current_step,current_position = item
            if current_step%2==1:
                reachable_in_odd_steps.add(current_position)
            for d in D:
                next_position = current_position+d
                next_step = current_step+1
                _x = next_position.real%mod_x
                _y = next_position.imag%mod_y
                __next_position = _x+_y*1j
                
                if grounds[__next_position] == '#':
                    continue
                if next_position not in visited:
                    visited.add(next_position)
                    if next_step>steps_target:
                        discarded.add( (next_step,next_position) )
                    else:
                        queue.append( (next_step,next_position) )
        return len(reachable_in_odd_steps)
    
    reachable_in_cycles = []
    for i in range(5):
        steps_target = i*mod_x+65
        reachable_in_cycles.append(find_reachable_in_steps(steps_target))
    
    cycles = 26501365//mod_x
    for i in range(len(reachable_in_cycles),cycles+1):
        reachable_in_cycles.append(
            reachable_in_cycles[i-2]
            + (reachable_in_cycles[i-2]-reachable_in_cycles[i-4])
            + (reachable_in_cycles[i-2]-reachable_in_cycles[i-4]) - 
              (reachable_in_cycles[i-4]-reachable_in_cycles[i-6])
        )
    return reachable_in_cycles[cycles]
