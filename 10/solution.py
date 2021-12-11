import queue

def parse(lines):
    lines = [l.strip() for l in lines]
    return lines
        
points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def main(arg):
    lines = parse(arg)
    score = 0
    completion_scores = []
    for l in lines:
        corrupted = False
        stack = []
        for b in l:
            if b in '([{<':
                stack.append(b)
            elif b in ')]}>':
                pair = stack.pop()
                if not pair + b in ['()', '[]', '{}', '<>']:
                    score += points[b]
                    corrupted = True
                    break
        if not corrupted:
            sc = 0
            for b in reversed(stack):
                sc *= 5
                sc += '([{<'.index(b) + 1
            completion_scores.append(sc)
    print(score)
    completion_scores.sort()
    print(completion_scores[len(completion_scores)//2])
                    

TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
