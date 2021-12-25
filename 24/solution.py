import inspect
import math


def parse(lines):
    p1 = [int(i) for i in lines[0].strip().split('\t')]
    p2 = [int(i) for i in lines[1].strip().split('\t')]
    divisors = [int(i) for i in lines[2].strip().split('\t')]
    return p1, p2, divisors


def getZ(p1, p2, z, w, divisor):
    v = 1 if (z % 26 + p1) != w else 0
    result = (z // divisor) * (25 * v + 1) + (w + p2) * v
    return result


def isPossible(p1, p2, divisors, last_z, smallest=False):
    if p1[0] < 10:
        next_w = last_z % 26 + p1[0]
        if next_w in range(1, 10):
            next_z = getZ(p1[0], p2[0], last_z, next_w, divisors[0])
            if len(p1) == 1 and next_z == 0:
                return True,[next_w]
            elif len(p1) == 1:
                return False
            else:
                pos = isPossible(p1[1:], p2[1:], divisors[1:], next_z, smallest)
                if pos:
                    return True, [next_w] + pos[1]
    else:
        order = range(1, 10) if smallest else range(9, 0, -1)
        for next_w in order:
            next_z = getZ(p1[0], p2[0], last_z, next_w, divisors[0])
            pos = isPossible(p1[1:], p2[1:], divisors[1:], next_z, smallest)
            if pos:
                return True, [next_w] + pos[1]
    return False


def main(arg):
    p1, p2, divisors = parse(arg)

    res = isPossible(p1, p2, divisors, 0)
    print(''.join([str(r) for r in res[1]]))

    res = isPossible(p1, p2, divisors, 0, smallest=True)
    print(''.join([str(r) for r in res[1]]))


if __name__ == "__main__":
    with open("parameters.tsv") as f:
        INPUT = f.readlines()
    print("Input:")
    main(INPUT)
