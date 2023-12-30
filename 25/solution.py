from __future__ import annotations

import sys

from collections import defaultdict, deque


def parse_input(file_handle) -> defaultdict[str,set[str]]:
    graph = defaultdict(set)
    for line in (l.strip() for l in file_handle.readlines()):
        node1,_nodes = line.split(': ')
        nodes = _nodes.split(' ')
        for node2 in nodes:
            graph[node1].add(node2)
            graph[node2].add(node1)
    return graph


def find_sub_graph_size(graph:defaultdict[str,set[str]], node:str) -> int:
    queue:deque[str] = deque()
    queue.append(node)
    found = set([node])
    while queue:
        node1 = queue.popleft()
        for node2 in graph[node1]:
            if node2 not in found:
                found.add(node2)
                queue.append(node2)
    return len(found)


def star1(problem_input:defaultdict[str,set[str]]) -> int:
    problem_input['xqh'].remove('ssd')
    problem_input['ssd'].remove('xqh')
    problem_input['mqb'].remove('qlc')
    problem_input['qlc'].remove('mqb')
    problem_input['khn'].remove('nrs')
    problem_input['nrs'].remove('khn')
    a = find_sub_graph_size(problem_input, 'xqh')
    b = find_sub_graph_size(problem_input, 'ssd')
    return a*b


def star2(problem_input):
    return None


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
