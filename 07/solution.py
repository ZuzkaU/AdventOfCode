def parse(lines):
    nums = list(map(int, lines[0].strip().split(',')))
    return nums

def sum_dist(k):
    return int(k * (k+1) / 2)

def main(arg):
    nums = parse(arg)
    sorted_nums = sorted(nums)
    median = sorted_nums[len(nums)//2]
    print(sum([abs(n - median) for n in nums]))

    position = sorted_nums[0]
    cost = sum([sum_dist(abs(i - position)) for i in sorted_nums])
    while True:
        position += 1
        new_cost = sum([sum_dist(abs(i - position)) for i in sorted_nums])
        if new_cost < cost:
            cost = new_cost
        else:
            break
    print(cost)
                
                    

TEST_INPUT = """16,1,2,0,4,2,7,1,2,14""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
