def parse(lines):
    fish = map(int, lines[0].strip().split(','))
    return fish

def dummy_main(arg):
    fish = parse(arg)
    for day in range(80):
        new_fish = []
        for f in fish:
            if f == 0:
                new_fish.append(6)
                new_fish.append(8)
            else:
                new_fish.append(f-1)
        fish = new_fish
    print(len(fish))

def main(arg):
    fish = parse(arg)
    counts = {i: 0 for i in range(9)}
    for f in fish:
        counts[f] += 1
    for day in range(80):
        new_counts = {i: 0 for i in range(9)}
        for d in counts.keys():
            if d == 0:
                new_counts[6] += counts[0]
                new_counts[8] += counts[0]
            else:
                new_counts[d-1] += counts[d]
        counts = new_counts
    total = sum(counts.values())
    print(total)
    
    for day in range(80, 256):
        new_counts = {i: 0 for i in range(9)}
        for d in counts.keys():
            if d == 0:
                new_counts[6] += counts[0]
                new_counts[8] += counts[0]
            else:
                new_counts[d-1] += counts[d]
        counts = new_counts
    total = sum(counts.values())
    print(total)

TEST_INPUT = """3,4,3,1,2""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    main(TEST_INPUT)
    main(INPUT)
