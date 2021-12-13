import networkx as nx

def parse(lines):
    G = nx.Graph()
    for l in lines:
        nodes = l.strip().split('-')
        for n in nodes:
            if not n in G:
                s = "small" if n == n.lower() else "big"
                G.add_node(n, size=s)
        G.add_edge(nodes[0], nodes[1])
    return G


def main(arg):
    G = parse(arg)
    paths = [['start']]
    finished = 0
    while not paths == []:
        new_paths = []
        for p in paths:
            for n in G.neighbors(p[-1]):
                if G.nodes[n]["size"] == "small" and n in p:
                    continue
                elif n == "end":
                    finished += 1
                else:
                    new_paths.append(p + [n])
        paths = new_paths
    print(finished)
    
    
    paths = [(['start'], False)]
    finished = 0
    # DFS would be better because it doesn't have to store all the paths
    while not paths == []:
        new_paths = []
        for (p, visited_twice) in paths:
            for n in G.neighbors(p[-1]):
                if n == "start":
                    continue
                elif n == "end":
                    finished += 1
                elif G.nodes[n]["size"] == "small" and n in p and not visited_twice:
                    new_paths.append((p + [n], True))
                elif G.nodes[n]["size"] == "small" and n in p and visited_twice:
                    continue
                else:
                    new_paths.append((p + [n], visited_twice))
        paths = new_paths
    print(finished)


TEST_INPUT = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
