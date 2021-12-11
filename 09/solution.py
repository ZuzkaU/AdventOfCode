import queue

def parse(lines):
    lines = [l.strip() for l in lines]
    world = [[9] * (len(lines[0])+2) for i in range(len(lines)+2)]
    for i, l in enumerate(lines):
        for j, n in enumerate(l):
            world[i+1][j+1] = int(n)
    return world
    
def bfs(i, j, world, mark):
    q = queue.Queue()
    q.put((i, j))
    size = 0
    while not q.empty():
        (i, j) = q.get()
        if not mark[i][j] and world[i][j] < 9:
            size += 1
            mark[i][j] = True
            q.put((i+1, j))
            q.put((i-1, j))
            q.put((i, j+1))
            q.put((i, j-1))
    return size
    

def main(arg):
    world = parse(arg)
    danger = 0
    for i in range(1, len(world)-1):
        for j in range(1, len(world[0])-1):
            if world[i-1][j] > world[i][j] and \
               world[i+1][j] > world[i][j] and \
               world[i][j-1] > world[i][j] and \
               world[i][j+1] > world[i][j]:
                danger += 1 + world[i][j]
    print(danger)
    
    mark = [[False] * len(world[0]) for i in range(len(world))]
    basins = []
    for i in range(1, len(world)-1):
        for j in range(1, len(world[0])-1):
            if world[i][j] < 9 and not mark[i][j]:
                basin = bfs(i, j, world, mark)
                basins.append(basin)
    basins.sort()
    print(basins[-3] * basins[-2] * basins[-1])
                    

TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
