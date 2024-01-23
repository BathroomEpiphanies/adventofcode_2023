from __future__ import annotations


def parse_input(file_handle) -> list[tuple[str,int,str]]:
    digs = []
    for line in (l.strip() for l in file_handle.readlines()):
        d,l,c = line.split(' ')
        digs.append( (d,int(l),c[1:-1]) )
    return digs


def integrate_trench(dig_instructions:list[tuple[str,int]]):
    # The enclosed area is the integral under segments going to the right, minus
    # segments going left. Half of the border length lies outside the center
    # line of the circumference, and needs to be added. Circumference is always
    # even since equal steps needs to be taken left/right and down/up There are
    # also 4 more convex corners than concave corners, this adds another 1.
    height = 0
    circumference = 0
    integral = 0
    for direction,length in dig_instructions:
        circumference += length
        if direction == 'R':
            integral += length*height
        if direction == 'L':
            integral -= length*height
        if direction == 'U':
            height += length
        if direction == 'D':
            height -= length
    return integral+circumference//2+1


def part1(problem_input:list[tuple[str,int,str]]) -> int:
    dig_instructions = [(d,l) for d,l,*_ in problem_input]
    return integrate_trench(dig_instructions)


def part2(problem_input:list[tuple[str,int,str]]) -> int:
    directions = {'0':'R', '1':'D', '2':'L', '3':'U'}
    dig_instructions = [(directions[color[-1]],int(color[1:-1],16)) for _,_,color in problem_input]
    return integrate_trench(dig_instructions)
