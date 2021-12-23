import inspect
import itertools
import math
import re


def parse(lines):
    players = []
    for l in lines:
        res = re.findall("[0-9]+", l)
        players.append((int(res[0]), int(res[1]), 0))
    return players


def main(arg):
    players = parse(arg)
    dice = itertools.cycle(range(1, 101))
    rolls_counter = 0
    n = 0
    while True:
        (player, pos, score) = players[n]
        roll = next(dice) + next(dice) + next(dice)
        rolls_counter += 3
        new_pos = (pos + roll) % 10 or 10
        score += new_pos
        players[n] = (player, new_pos, score)
        if score >= 1000:
            (_, _, s) = players[1-n]
            print(s * rolls_counter)
            break
        n = 1-n

    players = parse(arg)
    _, pos1, _ = players[0]
    _, pos2, _ = players[1]
    dirac_dice = list(zip(range(3, 10), [1, 3, 6, 7, 6, 3, 1]))
    universes = [(0, 1, (pos1, 0), (pos2, 0))]
    wins = [0, 0]
    while not universes == []:
        n, uni, (p1, s1), (p2, s2) = universes.pop()
        for (roll, u) in dirac_dice:
            if n == 0:
                new_pos = (p1 + roll) % 10 or 10
                score = s1 + new_pos
                new_tuple = (1-n, uni*u, (new_pos, score), (p2, s2))
            else:
                new_pos = (p2 + roll) % 10 or 10
                score=s2+new_pos
                new_tuple = (1-n, uni*u, (p1, s1), (new_pos, score))
            if score >= 21:
                wins[n] += uni*u
            else:
                universes.append(new_tuple)
    print(wins)


TEST_INPUT = """Player 1 starting position: 4
Player 2 starting position: 8""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)