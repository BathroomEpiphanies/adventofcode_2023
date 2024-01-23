from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations, count, cycle, product


def parse_input(file_handle) -> BrickPile:
    bricks = []
    for line,name in zip((l.strip() for l in file_handle.readlines()), count(1)):
        _corner1,_corner2 = line.split('~')
        corner1 = Coord(*(int(n) for n in _corner1.split(',')))
        corner2 = Coord(*(int(n) for n in _corner2.split(',')))
        bricks.append(Brick(corner1, corner2, str(name)))
    return BrickPile(bricks)


@dataclass
class Coord:
    x:int
    y:int
    z:int


@dataclass
class Brick:
    c1:Coord
    c2:Coord
    name:str
    
    def __init__(self, c1, c2, name):
        self.c1 = c1
        self.c2 = c2
        self.xrange = list(range(min(c1.x,c2.x), max(c1.x,c2.x)+1))
        self.yrange = list(range(min(c1.y,c2.y), max(c1.y,c2.y)+1))
        self.zrange = list(range(min(c1.z,c2.z), max(c1.z,c2.z)+1))
        self.name = name
    
    def move_down(self, steps:int) -> None:
        self.c1.z -= steps
        self.c2.z -= steps
        self.zrange = [z-steps for z in self.zrange]
    
    def __hash__(self) -> int:
        return id(self)
    
    def free_drop_distance_to(self, other:Brick) -> None|int:
        if other is self:
            return None
        if any(x1==x2 for x1,x2 in product(self.xrange, other.xrange)) and \
           any(y1==y2 for y1,y2 in product(self.yrange, other.yrange)):
            return self.zrange[0] - other.zrange[-1] - 1
        return None


@dataclass
class BrickPile:
    
    def __init__(self, bricks:list[Brick]) -> None:
        self.bricks = bricks
        self.overlap:dict[Brick,set[Brick]] = defaultdict(set)
        self.supporters:dict[Brick,set[Brick]] = {} #defaultdict(set)
        
        self.minx = min(min(b.xrange) for b in self.bricks)
        self.maxx = max(max(b.xrange) for b in self.bricks)
        self.miny = min(min(b.yrange) for b in self.bricks)
        self.maxy = max(max(b.yrange) for b in self.bricks)
        self.minz = min(min(b.zrange) for b in self.bricks)
        self.maxz = max(max(b.zrange) for b in self.bricks)
        bricks.insert(0, Brick(Coord(self.minx,self.miny,0), Coord(self.maxx,self.maxy,0), '-'))
        for brick1,brick2 in combinations(self.bricks, 2):
            drop = brick1.free_drop_distance_to(brick2)
            if drop is not None and drop>=0:
                self.overlap[brick1].add(brick2)
            if drop is not None and drop<0:
                self.overlap[brick2].add(brick1)
    
    def compact_pile(self):
        self.bricks.sort(key=lambda b: b.zrange[0])
        changed = True
        while changed:
            changed = False
            for brick1 in self.bricks[1:]:
                free_drop_distances = []
                for brick2 in self.overlap[brick1]:
                    free_drop_distance = brick1.free_drop_distance_to(brick2)
                    free_drop_distances.append(free_drop_distance)
                free_drop_distance = min(free_drop_distances)
                if free_drop_distance>0:
                    brick1.move_down(free_drop_distance)
                    changed = True
    
    def find_supporters(self):
        for brick1 in self.bricks[1:]:
            self.supporters[brick1] = set()
            for brick2 in (b for b in self.overlap[brick1] if b.zrange[0]>0):
                if brick1.free_drop_distance_to(brick2) == 0:
                    self.supporters[brick1].add(brick2)
    
    def plot(self) -> None:
        output = [['.' for _ in range(self.maxx+1)] for _ in range(self.maxz+1)]
        print()
        for brick in self.bricks:
            for x,z in product(brick.xrange, brick.zrange):
                output[z][x] = brick.name
        for row in reversed(output):
            print(''.join(str(c) for c in row))
        output = [['.' for _ in range(self.maxy+1)] for _ in range(self.maxz+1)]
        print()
        for brick in self.bricks:
            for y,z in product(brick.yrange, brick.zrange):
                output[z][y] = brick.name
        for row in reversed(output):
            print(''.join(str(c) for c in row))


def part1(problem_input:BrickPile) -> int:
    problem_input.compact_pile()
    problem_input.find_supporters()
    single_supporters = set()
    for brick in problem_input.bricks[1:]:
        if len(problem_input.supporters[brick])<=1:
            single_supporters |= problem_input.supporters[brick]
    return len(problem_input.bricks)-1 - len(single_supporters)


def part2(problem_input:BrickPile) -> int:
    problem_input.compact_pile()
    problem_input.find_supporters()
    for brick,supporter in problem_input.supporters.items():
        if not supporter:
            supporter.add(problem_input.bricks[0])
    
    total = 0
    for brick1 in problem_input.bricks[1:]:
        supporter_copy = {b:{t for t in s} for b,s in problem_input.supporters.items()}
        to_remove = {brick1}
        while to_remove:
            for b in to_remove:
                del(supporter_copy[b])
            new_to_remove = set()
            for brick2,supporters in supporter_copy.items():
                supporters -= to_remove
                if not(supporters):
                    new_to_remove.add(brick2)
            to_remove = new_to_remove
        total += len(problem_input.bricks)-len(supporter_copy)-2
    return total
