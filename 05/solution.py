def init():
    with open("input.txt") as f:
        lines = f.readlines()
        raw_vents = [l.strip().split(' -> ') for l in lines]
        str_vents = [(tuple(a.split(',')), tuple(b.split(','))) for [a, b] in raw_vents]
        vents = [((int(a), int(b)), (int(c), int(d))) for ((a, b), (c, d)) in str_vents]
        world = [[0]*1000 for i in range(1000)]
        return world, vents

if __name__ == "__main__":
    world, vents = init()
    for ((a, b), (c, d)) in vents:
        if a == c:
            for i in range(min(b, d), max(b, d)+1):
                world[a][i] += 1
        elif b == d:
            for i in range(min(a, c), max(a, c)+1):
                world[i][b] += 1
    count = 0
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] >= 2:
                count += 1
    print(count)
    
    for ((a, b), (c, d)) in vents:
        if not a == c and not b == d:
            for i in range(0, max(b, d)+1 - min(b, d)):
                world[a + i if c>a else a - i][b + i if d>b else b - i] += 1
    count = 0
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] >= 2:
                count += 1
    print(count)
