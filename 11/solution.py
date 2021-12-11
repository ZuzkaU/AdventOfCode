def parse(lines):
    octopuses = [[int(i) for i in l.strip()] for l in lines]
    return Octop(octopuses)

class Octop:
    def __init__(self, octopuses):
        self.octopuses = octopuses
        self.flashed = [[False] * 10 for i in range(10)]
        self.to_flash = []
        self.flash_count = 0
    
    def step(self):
        self.flashed = [[False] * 10 for i in range(10)]
        self.to_flash = []
        for i in range(10):
            for j in range(10):
                self.octopuses[i][j] += 1
                if self.octopuses[i][j] >= 10:
                    self.to_flash.append((i, j))
        
        while not self.to_flash == []:
            (i, j) = self.to_flash.pop()
            self.flash(i, j)
    
    def flash(self, i, j):
        if self.flashed[i][j]:
            return
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if i + dx < 0 or j + dy < 0 or i + dx > 9 or j + dy > 9:
                    continue
                if self.flashed[i + dx][j + dy]:
                    continue
                self.octopuses[i + dx][j + dy] += 1
                if self.octopuses[i + dx][j + dy] >= 10:
                    self.to_flash.append((i + dx, j + dy))
        self.flashed[i][j] = True
        self.octopuses[i][j] = 0
        self.flash_count += 1
    
    def __str__(self):
        string = ""
        for l in self.octopuses:
            for o in l:
                string += str(o)
            string += '\n'
        return string
    
    def all_flashed(self):
        return all([all(self.flashed[i]) for i in range(10)])


def main(arg):
    octopuses = parse(arg)
    flashes = 0
    for step in range(100):
        octopuses.step()
    print(octopuses.flash_count)
    
    step = 100
    while True:
        octopuses.step()
        step += 1
        if octopuses.all_flashed():
            break
    print(step)
                    

TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
