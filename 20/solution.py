import inspect
import math


def parse(lines):
    enhancement = lines[0]
    pic = []
    for l in lines[2:]:
        pic.append([0 if c == '.' else 1 for c in l.strip()])
    return pad(pic, 105), enhancement


def pad(pic, n):
    padded = [[0] * (len(pic[0]) + 2 * n) for i in range(n)]
    for l in pic:
        new_line = [0] * n + l + [0] * n
        padded.append(new_line)
    padded += [[0] * (len(pic[0]) + 2 * n) for i in range(n)]
    return padded


def enhance(pic, enhancement):
    enhanced = []
    x, y = len(pic), len(pic[0])
    for i in range(x):
        if not 0 < i < x-1:
            continue
        new_line = []
        for j in range(y):
            if not 0 < j < y-1:
                continue
            index = ''.join(map(str, pic[i-1][j-1:j+2] + pic[i][j-1:j+2] + pic[i+1][j-1:j+2]))
            index = int(index, base=2)
            new_line.append(1 if enhancement[index] == '#' else 0)
        enhanced.append(new_line)
    return enhanced


def print_pic(pic):
    for l in pic:
        for c in l:
            print('.' if c == 0 else '#', end='')
        print()


def main(arg):
    picture, enhancement = parse(arg)
    for i in range(2):
        picture = enhance(picture, enhancement)
    count = 0
    for l in picture:
        for n in l:
            count += n
    print(count)


    for i in range(48):
        picture = enhance(picture, enhancement)
    count = 0
    for l in picture:
        for n in l:
            count += n
    print(count)


TEST_INPUT = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
