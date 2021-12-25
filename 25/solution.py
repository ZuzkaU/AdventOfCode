import inspect
import math


def parse(lines):
    m = []
    for l in lines:
        m.append(list(l.strip()))
    return m


def main(arg):
    m = parse(arg)
    moved = True
    count = 0
    while moved:
        moved = False
        for i in range(len(m)):
            new_line = m[i].copy()
            for j in range(len(m[0])):
                if m[i][j] == '>' and m[i][(j + 1) % len(m[0])] == '.':
                    new_line[j] = '.'
                    new_line[(j + 1) % len(m[0])] = '>'
                    moved = True
            m[i] = new_line
        for j in range(len(m[0])):
            new_column = [m[i][j] for i in range(len(m))]
            for i in range(len(m)):
                if m[i][j] == 'v' and m[(i+1) % len(m)][j] == '.':
                    new_column[i] = '.'
                    new_column[(i+1) % len(m)] = 'v'
                    moved = True
            for i in range(len(m)):
                m[i][j] = new_column[i]

        count += 1
    print(count)


TEST_INPUT = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
