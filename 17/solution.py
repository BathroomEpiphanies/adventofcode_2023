from __future__ import annotations

import sys

from dataclasses import dataclass
from enum import Enum
from queue import PriorityQueue


def parse_input(file_handle) -> Graph:
    return Graph({x+y*1j:int(n) for y,row in enumerate(l.strip() for l in file_handle.readlines()) for x,n in enumerate(row)})


class DIR(complex, Enum):
    R = +1+0j
    D = +0+1j
    U = +0-1j
    L = -1+0j
    
    def __str__(self) -> str:
        return self.name
    __repr__ = __str__


class Graph:
    
    def __init__(self, heatloss_map:dict[complex,int]) -> None:
        self.heatloss_map = heatloss_map
        self.maxx = round(max(p.real for p in self.heatloss_map))
        self.maxy = round(max(p.imag for p in self.heatloss_map))
        self.__edges = {}
    
    @dataclass
    class Node:
        position:complex
        history:tuple(complex,complex,complex)
        def __hash__(self) -> int:
            return hash((self.position,self.history))
    
    def minimize_heatloss(self):
        
        @dataclass
        class QueueItem:
            heatloss:int
            node:complex
            history:list[complex]
            def __lt__(self, other:QueueItem) -> bool:
                return self.heatloss < other.heatloss
        
        source = self.Node(0,(0,0,0))
        goal = self.maxx+self.maxy*1j
        found = set()
        found.add(source)
        queue = PriorityQueue()
        queue.put(QueueItem(0,source,[0]))
        while not queue.empty():
            item = queue.get()
            if item.node.position == goal:
                break
            for node2,heatloss in self[item.node].items():
                if not node2 in found:
                    found.add(node2)
                    queue.put(QueueItem(item.heatloss+heatloss, node2, item.history+[node2.position]))
        print(item.history)
        return item.heatloss
    
    def clear(self):
        self.__edges = {}
    
    def __getitem__(self, node):
        if node not in self.__edges:
            self.__edges[node] = self.generate_edges(node)
        return self.__edges[node]
    
    def generate_edges_star1(self, node:Node) -> dict[Node,int]:
        edges = {}
        for d in DIR:
            if node.position+d not in self.heatloss_map or \
                -d==node.history[-1] or \
                all(d==h for h in node.history[-3:]):
                continue
            edges[Graph.Node(node.position+d, (*node.history,d)[-3:])] = self.heatloss_map[node.position+d]
        return edges
    
    def generate_edges_star2(self, node:Node) -> dict[Node,int]:
        edges = {}
        for d in DIR:
            if d==node.history[-1] or -d==node.history[-1]:
                continue
            for distance in range(4,11):
                if node.position+distance*d in self.heatloss_map:
                    edges[Graph.Node(node.position+distance*d, (distance,d))] = \
                        sum(hl for hl in (self.heatloss_map[node.position+(e+1)*d] for e in range(distance)))
        return edges


def star1(problem_input:Graph) -> int:
    problem_input.clear()
    problem_input.generate_edges = problem_input.generate_edges_star1
    return problem_input.minimize_heatloss()


def star2(problem_input:Graph) -> int:
    problem_input.clear()
    problem_input.generate_edges = problem_input.generate_edges_star2
    return problem_input.minimize_heatloss()


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
