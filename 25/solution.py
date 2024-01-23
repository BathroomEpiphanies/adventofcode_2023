from __future__ import annotations

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


def part1(problem_input:defaultdict[str,set[str]], *metadata:str) -> int:
    bridges = [i.split(' ') for i in metadata[:-1]]
    representatives = metadata[-1].split(' ')
    for a,b in bridges:
        problem_input[a].remove(b)
        problem_input[b].remove(a)
    n = find_sub_graph_size(problem_input, representatives[0])
    m = find_sub_graph_size(problem_input, representatives[1])
    return n*m
