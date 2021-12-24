import inspect
import math
import re
import networkx as nx
import heapq


def parse(lines):
    return Node([list(l) for l in lines], 0, None)


class Node:
    def __init__(self, lines, cost, parent):
        self.lines = lines
        self.neighbors = None
        self.cost = cost
        self.parent = parent

    def findNeighbors(self):
        self.neighbors = []
        for x in [2, 3]:
            for y in [3, 5, 7, 9]:
                new_states = self.moveFromHouse(x, y)
                if new_states:
                    self.neighbors += new_states
        x = 1
        for y in range(1, 12):
            new_state = self.moveHome(x, y)
            if new_state:
                self.neighbors.append(new_state)

    def __str__(self):
        return '\n'.join([''.join(l) for l in self.lines])

    def moveFromHouse(self, x, y):
        amphipod_type = self.lines[x][y]
        if amphipod_type not in 'ABCD':
            return None
        cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
        home = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
        if x == 3 and y == home[amphipod_type]:
            return None
        elif x == 2 and y == home[amphipod_type] and self.lines[3][y] == amphipod_type:
            return None

        moves = 0
        new_states = []
        if x == 3 and not self.lines[2][y] == '.':
            return None
        moves += x - 1
        for new_y in [1, 2, 4, 6, 8, 10, 11]:
            if all([c == '.' for c in self.lines[1][min(new_y, y):max(new_y, y) + 1]]):
                new_lines = self.swap(x, y, 1, new_y)
                price = (moves + max(new_y, y) - min(new_y, y)) * cost[amphipod_type]
                new_states.append((Node(new_lines, self.cost + price, self), price))
        return new_states

    def moveHome(self, x, y):
        home = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
        amphipod_type = self.lines[x][y]
        if amphipod_type not in 'ABCD':
            return None
        cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
        if (y < home[amphipod_type] and all([c == '.' for c in self.lines[1][y+1:home[amphipod_type]+1]])) or \
                (y > home[amphipod_type] and all([c == '.' for c in self.lines[1][home[amphipod_type]:y]])):
            if self.lines[2][home[amphipod_type]] == '.':
                if self.lines[3][home[amphipod_type]] == '.':
                    new_lines = self.swap(x, y, 3, home[amphipod_type])
                    price = (max(home[amphipod_type], y) - min(home[amphipod_type], y) + 2) * cost[amphipod_type]
                    return Node(new_lines, self.cost + price, self), price
                if self.lines[3][home[amphipod_type]] == amphipod_type:
                    new_lines = self.swap(x, y, 2, home[amphipod_type])
                    price = (max(home[amphipod_type], y) - min(home[amphipod_type], y) + 1) * cost[amphipod_type]
                    return Node(new_lines, self.cost + price, self), price
        return None

    def swap(self, x, y, new_x, new_y):
        new_lines = []
        for i, l in enumerate(self.lines):
            new_lines.append([])
            for j, c in enumerate(l):
                new_lines[i].append(c)
        c = new_lines[x][y]
        new_lines[x][y] = new_lines[new_x][new_y]
        new_lines[new_x][new_y] = c
        return new_lines

    def __eq__(self, other):
        return self.lines == other.lines

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return self.lines < other.lines

    def getHeuristics(self):
        min_cost = 0
        home = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
        cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
        for n, c in enumerate(self.lines[1]):
            if c in 'ABCD':
                min_cost += (abs(n - home[c]) + 1) * cost[c]
        for x in [2, 3]:
            for y in [3, 5, 7, 9]:
                c = self.lines[x][y]
                if c in 'ABCD' and not y == home[c]:
                    min_cost += (abs(y - home[c]) + 2) * cost[c]
        return min_cost

END = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########""".split('\n')


def main(arg):
    start = parse(arg)
    end = parse(END)

    h = [(0, start)]
    visited_states = set()
    minimal_cost = 100000
    while not h == []:
        (mincost_heur, node) = heapq.heappop(h)
        if node == end:
            print(node.cost)
            break
        if node in visited_states:
            continue
        visited_states.add(node)
        node.findNeighbors()
        for (n, _) in node.neighbors:
            heapq.heappush(h, (n.cost, n))
        if node.lines[1][1:-1] == ['.']*11:
            pass


TEST_INPUT = """#############
#...........#
###A#B#C#D###
  #B#A#C#D#
  #########""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
