def parse(lines):
    index = 0
    l = lines[index]
    dots = set()
    while not l.strip() == '':
        nums = l.strip().split(',')
        dots.add((int(nums[0]), int(nums[1])))
        index += 1
        l = lines[index]
    folds = []
    for l in lines[index+1:]:
        parts = l.split('=')
        folds.append((parts[0][-1], int(parts[1])))
    return dots, folds


def main(arg):
    dots, folds = parse(arg)
    for i, (axis, num) in enumerate(folds):
        new_dots = set()
        for (x, y) in dots:
            if axis == 'x':
                if x > num:
                    new_dots.add((2*num - x, y))
                else:
                    new_dots.add((x, y))
            elif axis == 'y':
                if y > num:
                    new_dots.add((x, 2*num - y))
                else:
                    new_dots.add((x, y))
        dots = new_dots
        if i == 0:
            print(len(dots))
    
    # folded paper boundaries:
    maxx, maxy = 0, 0
    for (x, y) in dots:
        maxx = max(x+1, maxx)
        maxy = max(y+1, maxy)
    
    paper = [['.'] * maxx for i in range(maxy)]
    for (x, y) in dots:
        paper[y][x] = '#'
    for line in paper:
        print(''.join(line))


TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
