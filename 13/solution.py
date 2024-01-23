from __future__ import annotations


def parse_input(file_handle) -> list[list[str]]:
    terrains:list[list[str]] = []
    terrain:list[str] = []
    for line in (l.strip() for l in file_handle.readlines()):
        if len(line)==0:
            terrains.append(terrain)
            terrain = []
            continue
        terrain.append(line)
    if terrain:
        terrains.append(terrain)
    return terrains


def find_mirror_value_with_smudge(terrain:list[str], smudges:int=0) -> int:
    
    def match_diff(string1:str, string2:str) -> int:
        return len([1 for c1,c2 in zip(string1,string2) if c1!=c2])
    
    def inner(terrain:list[str]) -> int:
        for row,_ in enumerate(terrain[1:], 1):
            if smudges == sum(match_diff(t1,t2) for t1,t2 in zip(reversed(terrain[:row]),terrain[row:])):
                return row
        return 0
    
    terrain_T = [''.join(t) for t in zip(*terrain)]
    return 100*inner(terrain)+inner(terrain_T)


def part1(problem_input) -> int:
    return sum(find_mirror_value_with_smudge(terrain, 0) for terrain in problem_input)


def part2(problem_input) -> int:
    return sum(find_mirror_value_with_smudge(terrain, 1) for terrain in problem_input)
