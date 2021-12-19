import math

def parse(lines):
    snailfish = []
    for l in lines:
        s = Snailfish(l.strip())
        snailfish.append(s)
    return snailfish


class Node:
    def __init__(self, string, parent):
        string = string.replace(' ', '')
        self.parent = parent
        self.l, self.r = None, None
        if string[1:string.index(',')].isdigit():
            self.l = int(string[1:string.index(',')])
        if string[(len(string)-string[::-1].index(',')):-1].isdigit():
            self.r = int(string[(len(string)-string[::-1].index(',')):-1])
        if self.l == None:
            brackets = 0
            for i, ch in enumerate(string[1:-1]):
                if ch == "[":
                    brackets += 1
                elif ch == "]":
                    brackets -= 1
                if brackets == 0:
                    self.l = Node(string[1:i+2], self)
                    if self.r == None:
                        self.r = Node(string[i+3:-1], self)
                    break
        elif self.r == None:
            self.r = Node(string[3:-1], self)
    
    def get_list(self):
        l = self.l if type(self.l) == int else self.l.get_list()
        r = self.r if type(self.r) == int else self.r.get_list()
        return [l, r]
    
    def get_magnitude(self):
        l = self.l if isinstance(self.l, int) else self.l.get_magnitude()
        r = self.r if isinstance(self.r, int) else self.r.get_magnitude()
        return 3*l + 2*r
    
    def explode(self, depth):
        if depth == 4:
            return True, self.l, self.r
        if isinstance(self.l, Node):
            exploded, l, r = self.l.explode(depth+1)
            if exploded:
                if not l == None and not r == None:
                    self.l = 0
                if r == None:
                    return exploded, l, None
                elif isinstance(self.r, int):
                    self.r += r
                    return exploded, l, None
                n = self.r
                while True:
                    if isinstance(n.l, Node):
                        n = n.l
                    else:
                        n.l += r
                        return exploded, l, None
        if isinstance(self.r, Node):
            exploded, l, r = self.r.explode(depth+1)
            if exploded:
                if not l == None and not r == None:
                    self.r = 0
                if l == None:
                    return exploded, None, r
                elif isinstance(self.l, int):
                    self.l += l
                    return exploded, None, r
                n = self.l
                while True:
                    if isinstance(n.r, Node):
                        n = n.r
                    else:
                        n.r += l
                        return exploded, None, r
        return False, None, None
        
    def split(self):
        if isinstance(self.l, int):
            if self.l >= 10:
                self.l = Node(str([math.floor(self.l/2), math.ceil(self.l/2)]), self)
                return True
        else:
            splitted = self.l.split()
            if splitted:
                return True
        if isinstance(self.r, int):
            if self.r >= 10:
                self.r = Node(str([math.floor(self.r/2), math.ceil(self.r/2)]), self)
                return True
        else:
            splitted = self.r.split()
            if splitted:
                return True
        return False
        

class Snailfish:
    def __init__(self, string):
        self.root = Node(string, None)

    def __add__(self, other):
        s = Snailfish(str([self.root.get_list(), other.root.get_list()]))
        s.reduce()
        return s

    def __str__(self):
        return str(self.root.get_list())

    def reduce(self):
        operations = [self.explode, self.split]
        while True:
            changed = False
            for op in operations:
                changed = op()
                if changed:
                    break
            if not changed:
                break
    
    def explode(self):
        exploded, _, _ = self.root.explode(0)
        return exploded
            
    
    def split(self):
        splitted = self.root.split()
        return splitted
    
    def magnitude(self):
        return self.root.get_magnitude()
            
    

def main(arg):
    snailfish = parse(arg)
    result = snailfish[0]
    for s in snailfish[1:]:
        result += s
    print(result.magnitude())
    
    magnitudes = []
    for a in snailfish:
        for b in snailfish:
            magnitudes.append((a+b).magnitude())
    print(max(magnitudes))


TEST_INPUT = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
