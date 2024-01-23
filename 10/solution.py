from __future__ import annotations

from collections import deque
from math import ceil


def parse_input(file_handle) -> PipeSystem:
    return PipeSystem([l.strip() for l in file_handle.readlines()])


class PipeSystem:
    
    directions = [+1+0j, +1+1j, -1+0j, +0-1j]
    redirect:dict[str,dict[complex,complex]] = {
        '|': {+0+1j:  0, +0-1j:  0},
        '-': {+1+0j:  0, -1+0j:  0},
        'L': {+0+1j: -1, -1+0j:  1},
        'J': {+0+1j:  1, +1+0j: -1},
        '7': {+1+0j:  1, +0-1j: -1},
        'F': {-1+0j: -1, +0-1j:  1},
        '.': {},
        'S': {},
    }
    
    def __init__(self, description:list[str]):
        self.pipe_system:dict[complex,str] = {x+y*1j:c for y,row in enumerate(description) for x,c in enumerate(row)}
        self.start_location:complex = next(p for p,c in self.pipe_system.items() if c=='S')
        self.visited,self.inside,self.cycle_length = self.__find_cycle()
        self.__expand_inside()
    
    @staticmethod
    def system_to_string(pipe_system:PipeSystem) -> str:
        xmax = round(max(p.real for p in pipe_system))
        ymax = round(max(p.imag for p in pipe_system))
        map_ = [''.join(str(pipe_system[x+y*1j]) if x+y*1j in pipe_system else '.'
                        for x in range(xmax+1)) for y in range(ymax+1)]
        return '\n'.join(''.join(str(n) for n in row) for row in map_)
    
    def __find_start_directions(self):
        # from start_point check in all directions if pipe there accepts incoming direction
        start_directions = []
        for direction in PipeSystem.directions:
            if self.start_location+direction in self.pipe_system:
                pipe_in_direction = self.pipe_system[self.start_location+direction]
                if direction in PipeSystem.redirect[pipe_in_direction]:
                    start_directions.append(direction)
        return start_directions
    
    def __find_cycle(self):
        start_direction = self.__find_start_directions()[0]
        direction_sum = 0
        visited = {self.start_location:'X'}
        queue = deque()
        queue.append( (0, self.start_location, start_direction) ) 
        inside_left = {self.start_location+start_direction*1j}
        inside_rght = {self.start_location+start_direction*-1j}
        while queue:
            distance,position,direction = queue.popleft()
            inside_left.add(position+direction*1j)
            inside_rght.add(position+direction*-1j)
            new_distance = distance + 1
            new_position = position + direction
            inside_left.add(new_position+direction*1j)
            inside_rght.add(new_position+direction*-1j)
            if new_position not in visited:
                turn = PipeSystem.redirect[self.pipe_system[new_position]][direction]
                direction_sum += turn
                new_direction = direction * 1j**turn
                visited[new_position] = 'X'
                queue.append( (new_distance, new_position, new_direction) )
        inside = {p:'I' for p in (inside_left if direction_sum>0 else inside_rght) if p not in visited}
        return visited,inside,distance
    
    def __expand_inside(self):
        queue = deque(p for p in self.inside)
        while queue:
            p = queue.popleft()
            for q in (p+d for d in PipeSystem.directions):
                if q not in self.inside and q not in self.visited:
                    self.inside[q] = 'I'
                    queue.append(q)


def part1(problem_input:PipeSystem) -> int:
    return ceil(problem_input.cycle_length/2)


def part2(problem_input:PipeSystem) -> int:
    #print(PipeSystem.system_to_string(problem_input.pipe_system))
    #print(PipeSystem.system_to_string(problem_input.visited))
    #print(PipeSystem.system_to_string(problem_input.inside))
    return len(problem_input.inside)
