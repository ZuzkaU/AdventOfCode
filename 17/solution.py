import re
import math

def parse(lines):
    x1, x2, y1, y2 = map(int, re.findall('-?\d+', lines[0]))
    return (x1, x2), (y1, y2)


def solve_quadratic_equation(a, b, c):
    dis = b**2-(4*a*c)
    if dis < 0:
        return None
    elif dis == 0:
        return [-b/(2*a)]
    else:
        return [(-b-math.sqrt(dis))/(2*a), (-b+math.sqrt(dis))/(2*a)]


def simulate(x, y, k):
    new_y = (k * (2*y-(k-1)))/2
    new_x = (k * (2*x-(k-1)))/2 if k<x else (x * (x+1)/2)
    return (new_x, new_y)


def main(arg):
    (min_x, max_x), (min_y, max_y) = parse(arg)
    max_drop = -min_y
    max_yvelocity = max_drop - 1
    max_height = (max_yvelocity * (max_yvelocity+1)) // 2
    print(max_height)
    
    counter = 0
    # min_xsteps: the smallest k, such that sum(1+2+...+k) >= min_x
    # it is the number of steps with the least possible x-velocity
    min_xsteps = math.ceil(solve_quadratic_equation(1, 1, -2*min_x)[1])
    # min_xvel: least possible velocity that reaches min_x
    min_xvel = math.ceil((2*min_x + min_xsteps**2 - min_xsteps) / (2 * min_xsteps))
    for yvel in range(min_y, max_yvelocity+1):
        min_ysteps = math.ceil(solve_quadratic_equation(1, -1-2*yvel, 2*max_y)[1])
        max_ysteps = math.floor(solve_quadratic_equation(1, -1-2*yvel, 2*min_y)[1])
        for xvel in range(min_xvel, max_x+1):
            counted = False
            for steps in range(min_ysteps, max_ysteps+1):
                (x, y) = simulate(xvel, yvel, steps)
                if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
                    counter += 1 if not counted else 0
                    counted = True
    print(counter)


TEST_INPUT = """target area: x=20..30, y=-10..-5""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
