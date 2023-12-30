from __future__ import annotations

import sys

from collections import defaultdict
from enum import Enum


def parse_input(file_handle) -> Forest:
    forest = {x+y*1j:t for y,row in enumerate(l.strip() for l in file_handle.readlines()) for x,t in enumerate(row)}
    maxx = round(max(p.real for p in forest))
    maxy = round(max(p.imag for p in forest))
    
    class D(complex, Enum):
        R = +1+0j
        U = +0-1j
        L = -1+0j
        D = +0+1j
    
    slope_rotate:dict[str,dict[complex,str]] = {
        '.': {D.R:'.', D.U:'.', D.L:'.', D.D:'.'},
        '>': {D.R:'>', D.L:'<'},
        '^': {D.U:'>', D.D:'<'},
        '<': {D.L:'>', D.R:'<'},
        'v': {D.D:'>', D.U:'<'},
    }
    
    start = 1+0j
    goal = maxx-1+maxy*1j
    visited = set()
    paths:defaultdict[complex,defaultdict[complex,int]] = defaultdict(lambda:defaultdict(int))
    def find_paths(departure:complex, position:complex) -> None:
        visited.add(departure)
        first_step = position-departure
        path = slope_rotate[forest[position]][first_step]
        while True:
            visited.add(position)
            options = {
                q for q in (position+d for d in D) \
                    if (q in paths and len(path)>1) \
                    or (q not in visited and forest.get(q,'#') != '#')
            }
            if len(options) != 1 or position in paths:
                if '<' in path and '>' not in path:
                    paths[position][departure] = len(path)
                elif '>' in path and '<' not in path:
                    paths[departure][position] = len(path)
                #elif all(p=='.' for p in path):
                #    paths[position][position] = len(path)
                #    paths[departure][position] = len(path)
                for option in options:
                    if option not in visited:
                        find_paths(position,option)
                return
            next_position = next(o for o in options)
            step = next_position-position
            position = next_position
            path += slope_rotate[forest[position]][step]
    find_paths(start, start+D.D)
    return Forest(paths, start, goal)


class Forest:
    
    def __init__(
            self, 
            paths:defaultdict[complex,defaultdict[complex,int]],
            start:complex,
            goal:complex,
    ) -> None:
        self.paths = paths
        self.start = start
        self.goal = goal
        self.longest_path = 0
    
    def find_longest_possible_path(self) -> int:
        """
        Is broken after refactoring. Gives the wrong answer to *2.
        """
        def find_paths_from(node, used_nodes):
            if node == self.goal:
                length = sum(self.paths[n1][n2] for n1,n2 in zip(used_nodes[:-1], used_nodes[1:]))
                self.longest_path = max(length, self.longest_path)
                return
            for destination in (d for d in self.paths[node] if d not in used_nodes):
                _used_nodes = [n for n in used_nodes]
                _used_nodes.append(destination)
                find_paths_from(destination, _used_nodes)
        find_paths_from(self.start, [self.start])
        return self.longest_path
    
    def remove_slopes(self) -> None:
        for node1,(node2,length) in list((n1,(n2,l)) for n1,es in self.paths.items() for n2,l in es.items()):
            self.paths[node2][node1] = length


def star1(problem_input:Forest) -> int:
    return problem_input.find_longest_possible_path()


def star2(problem_input:Forest) -> int:
    problem_input.remove_slopes()
    return problem_input.find_longest_possible_path()


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
