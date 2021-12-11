import itertools

def parse(lines):
    halves = [l.strip().split(' | ') for l in lines]
    examples = []
    for h in halves:
        examples.append((h[0].split(' '), h[1].split(' ')))
    return examples

def num_to_char(num):
    return chr(num + 97)

def char_to_num(ch):
    return ord(ch) - 97
    
def digit_to_segments(num):
    true_segments = {
        0: 'abcefg',
        1: 'cf',
        2: 'acdeg',
        3: 'acdfg',
        4: 'bcdf',
        5: 'abdfg',
        6: 'abdefg',
        7: 'acf',
        8: 'abcdefg',
        9: 'abcdfg'
        }
    return true_segments[num]
                
    

def shuffle(mapping, segments):
    new_segments = [mapping[ord(i)-97] for i in segments]
    return new_segments

def reverse(mapping, segments):
    original_segments = [chr(mapping.index(i)+97) for i in segments]
    return original_segments

def main(arg):
    examples = parse(arg)
    count = 0
    for (a, b) in examples:
        for seg in b:
            if len(seg) in [2, 3, 4, 7]:
                count += 1
    print(count)
    
    sumc = 0
    all_numbers = [set(digit_to_segments(num)) for num in range(10)]
    for (a, b) in examples:
        for mapping in itertools.permutations('abcdefg'):
            possible = True
            for digit in a:
                if not set(reverse(mapping, digit)) in all_numbers:
                    possible = False
                    break
            if possible:
                output_num = ''
                for digit in b:
                    true_segments = set(reverse(mapping, digit))
                    num = all_numbers.index(true_segments)
                    output_num += str(num)
                sumc += int(output_num)
                break
    print(sumc)
                    

TEST_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    main(TEST_INPUT)
    main(INPUT)
