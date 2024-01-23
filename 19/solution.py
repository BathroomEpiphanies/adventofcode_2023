from __future__ import annotations

import re

from copy import copy
from dataclasses import dataclass
from functools import reduce
from operator import mul


def parse_input(file_handle) -> tuple[dict[str,Workflow],list[Part]]:
    workflows = {}
    input_lines = (l.strip() for l in file_handle.readlines())
    for line in input_lines:
        if not line:
            break
        if match := re.match(r'([a-z]+){(.+)}', line):
            name,rules = match.groups()
        workflows[name] = Workflow.from_string(rules)
    workflows['A'] = ACCEPT
    workflows['R'] = REJECT
    
    parts = []
    for line in input_lines:
        parts.append(eval(f'Part({line[1:-1]})'))
    return workflows,parts


@dataclass
class Part:
    
    x:int
    m:int
    a:int
    s:int
    
    def eval_rule(self, rule:None|str) -> bool:
        if rule is None:
            return True
        return eval(f'self.{rule}')
    
    def __abs__(self) -> int:
        return self.x+self.m+self.a+self.s


class Workflow:
    
    def __init__(self, rules:list[tuple[None|str,str]]) -> None:
        self.rules = rules
    
    @staticmethod
    def from_string(string:str) -> Workflow:
        rules_ = string.split(',')
        default_rule = (None,rules_[-1])
        rules:list[tuple[None|str,str]] = [(f,t) for f,t,*_ in (r.split(':') for r in rules_[:-1])]
        rules.append(default_rule)
        return Workflow(rules)
    
    def __str__(self) -> str:
        return ' '.join(str(r) for r in self.rules)

ACCEPT = Workflow([])
REJECT = Workflow([])


def part1(problem_input:tuple[dict[str,Workflow],list[Part]]) -> int:
    workflows,parts = problem_input
    
    def evaluate_workflow_on_part(name:str, part:Part):
        if workflows[name] is ACCEPT:
            return True
        if workflows[name] is REJECT:
            return False
        for rule,target in workflows[name].rules:
            if part.eval_rule(rule):
                return evaluate_workflow_on_part(target, part)
        raise Exception('fell through')
    
    return sum(abs(part) for part in parts if evaluate_workflow_on_part('in', part))


@dataclass
class Ranges:
    
    x:list[int]
    m:list[int]
    a:list[int]
    s:list[int]
    
    def __abs__(self) -> int:
        diffs = [
            self.x[1] - self.x[0] + 1,
            self.m[1] - self.m[0] + 1,
            self.a[1] - self.a[0] + 1,
            self.s[1] - self.s[0] + 1,
        ]
        if any(d<=0 for d in diffs):
            return 0
        return reduce(mul, diffs)
    
    def apply_rule(self, rule:None|str, inverted:bool=False) -> Ranges:
        if rule is None:
            return self
        copy_ = Ranges(copy(self.x), copy(self.m), copy(self.a), copy(self.s))
        if match := re.match(r'([a-z]+)([<>])([0-9]+)', rule):
            parameter,operator,value_ = match.groups()
        value = int(value_)
        if operator == '<':
            if inverted:
                exec(f'copy_.{parameter}[0] = max(copy_.{parameter}[0], {value})')
            else:
                exec(f'copy_.{parameter}[1] = min(copy_.{parameter}[1], {value-1})')
        elif operator == '>':
            if inverted:
                exec(f'copy_.{parameter}[1] = min(copy_.{parameter}[1], {value})')
            else:
                exec(f'copy_.{parameter}[0] = max(copy_.{parameter}[0], {value+1})')
        return copy_


def part2(problem_input:tuple[dict[str,Workflow],list[Part]]) -> int:
    workflows,_ = problem_input
    
    accepted_ranges = []
    def find_accepted_ranges(name:str, ranges:Ranges):
        if workflows[name] is ACCEPT:
            accepted_ranges.append(ranges)
        for rule,target in workflows[name].rules:
            find_accepted_ranges(target, ranges.apply_rule(rule))
            ranges = ranges.apply_rule(rule, inverted=True)
    
    find_accepted_ranges('in', Ranges([1,4000], [1,4000], [1,4000], [1,4000]))
    return sum(abs(r) for r in accepted_ranges)
