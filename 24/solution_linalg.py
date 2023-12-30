from __future__ import annotations

import numpy as np
import sys
import z3

from dataclasses import dataclass
from itertools import combinations


def parse_input(file_handle) -> HailStorm:
    hail_stones = []
    for line in (l.strip() for l in file_handle.readlines()):
        _position,_velocity = line.split(' @ ')
        position = (int(n) for n in _position.split(', '))
        velocity = (int(n) for n in _velocity.split(', '))
        hail_stones.append(HailStone(*position,*velocity))
    if len(hail_stones) < 10:
        boundaries = (
            (7,7,0),
            (27,27,0),
        )
    else:
        boundaries = (
            (200_000_000_000_000,200_000_000_000_000,0),
            (400_000_000_000_000,400_000_000_000_000,0),
        )
    return HailStorm(hail_stones, boundaries)


@dataclass
class HailStorm:
    
    hail_stones:list[HailStone]
    boundaries:tuple[tuple[int,int,int],tuple[int,int,int]]
    
    def find_colliding_stones(self) -> int:
        colliding_paths = 0
        for stone1,stone2 in combinations(self.hail_stones, 2):
            crossing = stone1.time_of_crossing(stone2)
            if crossing is None:
                continue
            t1,t2 = crossing
            if t1<0 or t2<0:
                continue
            pos1 = stone1.position_at_time(t1)
            pos2 = stone2.position_at_time(t2)
            if all(self.boundaries[0][d] <= pos1[d] <= self.boundaries[1][d] for d in [0,1]) and \
               all(self.boundaries[0][d] <= pos2[d] <= self.boundaries[1][d] for d in [0,1]):
                colliding_paths += 1
        return colliding_paths
    
    def find_silver_bullet(self):
        solver = z3.Solver()
        px = [z3.Real(f'px{i}') for i,_ in enumerate(self.hail_stones)]
        py = [z3.Real(f'py{i}') for i,_ in enumerate(self.hail_stones)]
        pz = [z3.Real(f'pz{i}') for i,_ in enumerate(self.hail_stones)]
        vx = [z3.Real(f'vx{i}') for i,_ in enumerate(self.hail_stones)]
        vy = [z3.Real(f'vy{i}') for i,_ in enumerate(self.hail_stones)]
        vz = [z3.Real(f'vz{i}') for i,_ in enumerate(self.hail_stones)]
        t =  [z3.Real(f't{i}')  for i,_ in enumerate(self.hail_stones)]
        spx = z3.Real('spx')
        spy = z3.Real('spy')
        spz = z3.Real('spz')
        svx = z3.Real('vpx')
        svy = z3.Real('vpy')
        svz = z3.Real('vpz')
        for i,stone in enumerate(self.hail_stones):
            solver.add(px[i] == stone.px)
            solver.add(py[i] == stone.py)
            solver.add(pz[i] == stone.pz)
            solver.add(vx[i] == stone.vx)
            solver.add(vy[i] == stone.vy)
            solver.add(vz[i] == stone.vz)
            solver.add(px[i]+t[i]*vx[i] == spx+t[i]*svx)
            solver.add(py[i]+t[i]*vy[i] == spy+t[i]*svy)
            solver.add(pz[i]+t[i]*vz[i] == spz+t[i]*svz)
        solver.check()
        model = solver.model()
        total = 0
        for sp_ in [spx,spy,spz]:
            _sp = model.evaluate(sp_)
            total += float(_sp.as_fraction().numerator)/float(_sp.as_fraction().denominator)
        return round(total)


@dataclass
class HailStone:
    
    px:int
    py:int
    pz:int
    vx:int
    vy:int
    vz:int
    
    def time_of_crossing(self, other:HailStone) -> None|tuple[float,float]:
        try:
            solution = np.linalg.solve(
                [[self.vx,-other.vx],
                 [self.vy,-other.vy]],
                [-self.px+other.px, -self.py+other.py]
            )
        except np.linalg.LinAlgError:
            return None
        return (float(solution[0]),float(solution[1]))
    
    def position_at_time(self, time:float) -> tuple[float,float]:
        return (self.px+time*self.vx,self.py+time*self.vy)


def star1(problem_input:HailStorm) -> int:
    return problem_input.find_colliding_stones()


def star2(problem_input) -> int:
    return problem_input.find_silver_bullet()


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
