from __future__ import annotations


def parse_input(file_handle) -> list[str]:
    return [l.strip() for l in file_handle.readlines()]


def part1(problem_input:list[str]) -> int:
    sum:int = 0
    for line in problem_input:
        digits = [a for a in line if a in ['0','1','2','3','4','5','6','7','8','9']]
        sum += 10*int(digits[0]) + int(digits[-1])
    return sum


def find_first_number(string:str, reversed:bool=False):
    numbers = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    if reversed:
        numbers.update({
            'orez': 0, 'eno': 1, 'owt': 2, 'eerht': 3, 'ruof': 4,
            'evif': 5, 'xis': 6, 'neves': 7, 'thgie': 8, 'enin': 9,
        })
        string = string[::-1]
    else:
        numbers.update({
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
            'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        })
    for pos,_ in enumerate(string):
        for number,digit in numbers.items():
            if string[pos:pos+len(number)] == number:
                return digit


def part2(problem_input:list[str]) -> int:
    sum:int = 0
    for line in problem_input:
        sum += 10*find_first_number(line, reversed=False)
        sum += find_first_number(line, reversed=True)
    return sum
