from __future__ import annotations

from collections import defaultdict


def parse_input(file_handle) -> list[str]:
    return file_handle.readline().strip().split(',')


def hash(string:str) -> int:
    current_value = 0
    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


def part1(problem_input:list[str]) -> int:
    return sum(hash(s) for s in problem_input)    


def part2(problem_input:list[str]) -> int:
    # dict key insertion order is persistent on iteration
    boxes:dict[int,dict[str,int]] = defaultdict(dict)
    for lens in problem_input:
        if '=' in lens:
            name,focal_length = lens.split('=')
            boxes[hash(name)+1][name] = int(focal_length)
        elif '-' in lens:
            name,*_ = lens.split('-')
            try:
                del(boxes[hash(name)+1][name])
            except KeyError:
                pass
    return sum(
        box_number*lens_slot*focal_length \
        for box_number,box in boxes.items() \
        for lens_slot,(_,focal_length) in enumerate(box.items(), start=1)
    )
