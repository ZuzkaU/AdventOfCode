from collections import Counter

def dummy_parse(lines):
    polymer = lines[0].strip()
    rules = dict()
    for l in lines[2:]:
        parts = l.strip().split(' -> ')
        rules[parts[0]] = parts[1]
    return polymer, rules

def parse(lines):
    polymer = lines[0].strip()
    rules = dict()
    for l in lines[2:]:
        parts = l.strip().split(' -> ')
        rules[parts[0]] = parts[1]
    
    # make rules already contain 10 steps
    new_rules = dict()
    for j, pol in enumerate(rules.keys()):
        result = pol
        for i in range(20):
            print(j, i)
            new_pol = []
            previous_char = result[0]
            for ch in result[1:]:
                new_pol.append(previous_char)
                if previous_char + ch in rules.keys():
                    new_pol.append(rules[previous_char + ch])
                previous_char = ch
            new_pol.append(result[-1])
            result = new_pol
        new_rules[pol] = result
    
    return polymer, new_rules



def dummy_main(arg):
    polymer, rules = dummy_parse(arg)
    for i in range(10):
        new_pol = []
        previous_char = polymer[0]
        for ch in polymer[1:]:
            new_pol.append(previous_char)
            if previous_char + ch in rules.keys():
                new_pol.append(rules[previous_char + ch])
            previous_char = ch
        new_pol.append(polymer[-1])
        polymer = new_pol
    c = Counter(polymer)
    counts = c.most_common()
    (_, a), (_, b) = counts[0], counts[-1]
    print(a - b)


def main(arg):
    polymer, rules = dummy_parse(arg)
    
    c = Counter(a + b for (a, b) in zip(polymer[:-1], polymer[1:]))
    
    for i in range(40):
        new_c = Counter()
        for (pair, count) in c.most_common():
            if pair in rules.keys():
                new_c.update({pair[0] + rules[pair]: count})
                new_c.update({rules[pair] + pair[1]: count})
            else:
                new_c.update({pair:count})
        c = new_c
    
    letter_c = Counter()
    for (pair, count) in c.most_common():
        # if pair[0] == pair[1], the value in dict will be overriden,
        # so it's better to update both values separately
        letter_c.update({pair[0]: count})
        letter_c.update({pair[1]: count})
    true_letters = Counter()
    for (ch, count) in letter_c.most_common():
        ch_correction = [polymer[0], polymer[-1]].count(ch)
        true_letters.update({ch: (count + ch_correction) // 2 })
    
    counts = true_letters.most_common()
    (_, a), (_, b) = counts[0], counts[-1]
    print(a - b)


TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
