from __future__ import annotations

import sys
import z3

from dataclasses import dataclass
from itertools import combinations


def parse_input(file_handle) -> HailStorm:
    hail_stones = []
    for line in (l.strip() for l in file_handle.readlines()):
        _position,_velocity = line.split(' @ ')
        position = [int(n) for n in _position.split(', ')]
        velocity = [int(n) for n in _velocity.split(', ')]
        hail_stones.append(HailStone(position,velocity))
    if len(hail_stones) < 10:
        boundaries = (
            (7,7),
            (27,27),
        )
    else:
        boundaries = (
            (200_000_000_000_000,200_000_000_000_000),
            (400_000_000_000_000,400_000_000_000_000),
        )
    return HailStorm(hail_stones, boundaries)


def z3_to_float(model, var):
   _var = model.evaluate(var)
   return float(_var.as_fraction().numerator)/float(_var.as_fraction().denominator)


@dataclass
class HailStone:
    
    counter = 0
    
    def __init__(self, position, velocity) -> None:
        self.id_ = HailStone.counter
        HailStone.counter += 1
        
        self.px = z3.Real(f'px_{self.id_}')
        self.py = z3.Real(f'py_{self.id_}')
        self.pz = z3.Real(f'pz_{self.id_}')
        self.vx = z3.Real(f'vx_{self.id_}')
        self.vy = z3.Real(f'vy_{self.id_}')
        self.vz = z3.Real(f'vz_{self.id_}')
        
        self.constraints = []
        self.constraints.append(self.px == position[0])
        self.constraints.append(self.py == position[1])
        self.constraints.append(self.pz == position[2])
        self.constraints.append(self.vx == velocity[0])
        self.constraints.append(self.vy == velocity[1])
        self.constraints.append(self.vz == velocity[2])
    
    def position_at_time(self, time:z3.Real) -> tuple[z3.Real,z3.Real]:
        return (self.px+time*self.vx,self.py+time*self.vy)


class HailStorm:
    
    def __init__(
            self,
            hail_stones:list[HailStone],
            boundaries:tuple[tuple[int,int],tuple[int,int]]
    ):
        self.hail_stones = hail_stones
        self.minx = z3.Real('minx')
        self.miny = z3.Real('miny')
        self.maxx = z3.Real('maxx')
        self.maxy = z3.Real('maxy')
        self.constraints = []
        self.constraints.append(self.minx == boundaries[0][0])
        self.constraints.append(self.miny == boundaries[0][1])
        self.constraints.append(self.maxx == boundaries[1][0])
        self.constraints.append(self.maxy == boundaries[1][1])
    
    def collides(self, stone1:HailStone, stone2:HailStone) -> bool:
        solver = z3.Solver()
        for c in stone1.constraints:
            solver.add(c)
        for c in stone2.constraints:
            solver.add(c)
        for c in self.constraints:
            solver.add(c)
        stone1_t = z3.Real(f't_{stone1.id_}')
        stone2_t = z3.Real(f't_{stone2.id_}')
        solver.add(stone1.px+stone1_t*stone1.vx == stone2.px+stone2_t*stone2.vx)
        solver.add(stone1.py+stone1_t*stone1.vy == stone2.py+stone2_t*stone2.vy)
        solver.add(stone1_t>=0)
        solver.add(stone2_t>=0)
        solver.add(stone1.px+stone1_t*stone1.vx >= self.minx)
        solver.add(stone1.py+stone1_t*stone1.vy >= self.miny)
        solver.add(stone1.px+stone1_t*stone1.vx <= self.maxx)
        solver.add(stone1.py+stone1_t*stone1.vy <= self.maxy)
        solver.add(stone2.px+stone2_t*stone2.vx >= self.minx)
        solver.add(stone2.py+stone2_t*stone2.vy >= self.miny)
        solver.add(stone2.px+stone2_t*stone2.vx <= self.maxx)
        solver.add(stone2.py+stone2_t*stone2.vy <= self.maxy)
        #print(solver)
        #print()
        return solver.check() == z3.sat
    
    def count_colliding_stones(self) -> int:
        colliding_paths = 0
        l = len(self.hail_stones)
        l = (l*l-l)//2
        i = 0
        for stone1,stone2 in combinations(self.hail_stones, 2):
            if self.collides(stone1, stone2):
                colliding_paths += 1
        return colliding_paths
    
    def find_silver_bullet(self):
        solver = z3.Solver()
        t =  [z3.Real(f't{i}')  for i,_ in enumerate(self.hail_stones)]
        silver_px = z3.Real('px')
        silver_py = z3.Real('py')
        silver_pz = z3.Real('pz')
        silver_vx = z3.Real('vx')
        silver_vy = z3.Real('vy')
        silver_vz = z3.Real('vz')
        for i,stone in enumerate(self.hail_stones):
            for c in stone.constraints:
                solver.add(c)
            solver.add(stone.px+t[i]*stone.vx == silver_px+t[i]*silver_vx)
            solver.add(stone.py+t[i]*stone.vy == silver_py+t[i]*silver_vy)
            solver.add(stone.pz+t[i]*stone.vz == silver_pz+t[i]*silver_vz)
        #print(solver)
        solver.check()
        model = solver.model()
        return round(sum(z3_to_float(model, p_) for p_ in [silver_px,silver_py,silver_pz]))


def star1(problem_input:HailStorm) -> int:
    return problem_input.count_colliding_stones()


def star2(problem_input) -> int:
    return problem_input.find_silver_bullet()


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
