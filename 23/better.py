import inspect
import math
import re
import networkx as nx
import heapq


def parse(lines):
    hall = list(lines[1].strip()[1:-1])
    homes = [list(l.rstrip()[1:-1]) for l in lines[2:-1]]
    return State(hall, homes, 0, None)

NEW_LINES = """  #D#C#B#A#
  #D#B#A#C#""".split('\n')

def parse2(lines):
    lines.insert(3, NEW_LINES[1])
    lines.insert(3, NEW_LINES[0])
    hall = list(lines[1].strip()[1:-1])
    homes = [list(l.rstrip()[1:-1]) for l in lines[2:-1]]
    return State(hall, homes, 0, None)


COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HOME = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
HALL_POSITIONS = [0, 1, 3, 5, 7, 9, 10]
AMPIPHODES = 'ABCD'


class State:
    def __init__(self, hall, homes, cost, parent):
        self.hall = hall
        self.homes = homes
        self.cost = cost
        self.parent = parent

    def getNeighbors(self):
        neighbors = []

        # moving from home to hall
        for y, line in enumerate(self.homes):
            for x in HOME.values():
                if self.homes[y][x] not in AMPIPHODES:
                    continue
                amp = line[x]
                if all([self.homes[below][x] == amp for below in range(y, len(self.homes))]) and HOME[amp] == x:
                    continue
                if all([self.homes[above][x] == '.' for above in range(y)]):
                    for new_x in HALL_POSITIONS:
                        if all([c == '.' for c in self.hall[min(new_x, x):max(new_x, x) + 1]]):
                            neighbors.append(State.fromPrevious(self, new_x, x, y))

        # moving from hall to home
        for x, amp in enumerate(self.hall):
            if amp not in AMPIPHODES:
                continue
            for y, line in enumerate(self.homes):
                if all([self.homes[below][HOME[amp]] == amp for below in range(y+1, len(self.homes))]):
                    if all([self.homes[above][HOME[amp]] == '.' for above in range(y+1)]):
                        if all([c == '.' for c in self.hall[min(x, HOME[amp]) + 1:max(x, HOME[amp])]]):
                            neighbors.append(State.fromPrevious(self, x, HOME[amp], y))

        return neighbors



    @staticmethod
    def fromPrevious(state, hall_x, home_x, home_y):
        new_hall = state.hall.copy()
        new_homes = [h.copy() for h in state.homes]
        new_hall[hall_x] = state.homes[home_y][home_x]
        new_homes[home_y][home_x] = state.hall[hall_x]
        amph = new_hall[hall_x] if new_hall[hall_x] in AMPIPHODES else state.hall[hall_x]
        cost = state.cost + (abs(hall_x - home_x) + home_y + 1) * COST[amph]
        return State(new_hall, new_homes, cost, state)

    def __str__(self):
        homes = []
        for h in self.homes:
            homes.append(' '.join([h[x] for x in HOME.values()]))
        return 'HALL:' + ''.join(self.hall) + ', HOMES:' + ', '.join(homes)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return self.hall < other.hall

    def getHeuristics(self):
        min_cost = 0
        for n, c in enumerate(self.hall):
            if c in AMPIPHODES:
                    min_cost += (abs(n - HOME[c]) + 1) * COST[c]
        for line in self.homes:
            for x in HOME.values():
                if line[x] in AMPIPHODES and not x == HOME[line[x]]:
                    min_cost += (abs(x - HOME[line[x]]) + 2) * COST[line[x]]
        return min_cost

END = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########""".split('\n')

END2 = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".split('\n')


def aStar(start, end):
    h = [(0, start)]
    visited_states = set()
    while not h == []:
        (_, node) = heapq.heappop(h)
        if node == end:
            print(node.cost)
            break
        if node in visited_states:
            continue
        visited_states.add(node)
        for n in node.getNeighbors():
            heapq.heappush(h, (n.cost + n.getHeuristics(), n))


def main(arg):
    start = parse(arg)
    end = parse(END)

    aStar(start, end)

    start = parse2(arg)
    end = parse(END2)

    aStar(start, end)


TEST_INPUT = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
