import heapq

def parse(lines):
    graph = [[Node(None, i, j) for j in range(len(lines[0].strip())+2)] for i in range(len(lines)+2)]
    for i, l in enumerate(lines):
        for j, r in enumerate(l.strip()):
            graph[i+1][j+1] = Node(int(r), i+1, j+1)
    return graph

# it would be better to not make the whole map and just return the correct risk from the nodes
def new_parse(lines):
    height, width = len(lines), len(lines[0].strip())
    graph = [[Node(None, i, j) for j in range(width*5+2)] for i in range(height*5+2)]
    for i, l in enumerate(lines):
        for j, r in enumerate(l.strip()):
            for repeatx in range(5):
                for repeaty in range(5):
                    risk = int(r) + repeatx + repeaty
                    if risk > 9:
                        risk -= 9
                    x, y = repeatx*height + i+1, repeaty*width + j+1
                    graph[x][y] = Node(risk, x, y)
    return graph


class Node:
    def __init__(self, risk, x, y):
        self.risk = risk
        self.mock_node = (risk == None)
        self.sum_risk = None
        self.xy = (x, y)
        self.visited = False
        
    def enter(self, total_risk):
        if self.visited or self.mock_node:
            raise Exception('Cannot visit this node!')
        self.sum_risk = total_risk + self.risk
        self.visited = True
        
    def neighbor_xy(self):
        (x, y) = self.xy
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    
    # for the heap if the risk is equal
    def __lt__(self, other):
        return self.risk < other.risk
        

def dijkstra(graph, start):
    to_visit = []
    heapq.heappush(to_visit, (0 - start.risk, start))
    while len(to_visit) > 0:
        (path_len, node) = heapq.heappop(to_visit)
        if not node.visited and not node.mock_node:
            node.enter(path_len)
            for (x, y) in node.neighbor_xy():
                neighbor = graph[x][y]
                if not (neighbor.visited or neighbor.mock_node):
                    heapq.heappush(to_visit, (node.sum_risk, neighbor))
        if node == graph[-2][-2]:
            return


def main(arg):
    graph = parse(arg)
    dijkstra(graph, graph[1][1])
    print(graph[-2][-2].sum_risk)
    
    graph = new_parse(arg)
    print('parsed')
    dijkstra(graph, graph[1][1])
    print(graph[-2][-2].sum_risk)
    


TEST_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
