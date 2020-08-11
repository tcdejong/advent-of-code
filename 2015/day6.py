class LightGrid():
    def __init__(self, dim, part=1): 
        self.grid = [ [0] * dim for _ in range(dim)]
        self.part = part

    def __repr__(self):

        visual = "\n".join([str(row) for row in self.grid])
        visual = "\n".join([visual, f"Lit:   {self.count_lit()}", f"Unlit: {self.count_unlit()}"])

        return visual


    def count_lit(self):
        return sum(sum(_) for _ in self.grid)


    def count_unlit(self):
        return len(self.grid)**2 - self.count_lit()


    def change_to(self, x1, y1, x2, y2, val):
        x2 += 1
        y2 += 1
        for x in range(x1, x2):
            self.grid[x][y1:y2] = [val] * (y2-y1)


    def turn_on(self, x1, y1, x2, y2):
        self.change_to(x1, y1, x2, y2, 1)


    def turn_off(self, x1, y1, x2, y2):
        self.change_to(x1, y1, x2, y2, 0)


    def toggle(self, x1, y1, x2, y2):
        x2 += 1
        y2 += 1
        for x in range(x1, x2):
            self.grid[x][y1:y2] = [1 if i == 0 else 0 for i in self.grid[x][y1:y2]]


    def make_brighter(self, x1, y1, x2, y2):
        x2 += 1
        y2 += 1
        for x in range(x1, x2):
            self.grid[x][y1:y2] = [i+1 for i in self.grid[x][y1:y2]]


    def make_darker(self, x1, y1, x2, y2):
        x2 += 1
        y2 += 1
        for x in range(x1, x2):
            self.grid[x][y1:y2] = [i-1 if i > 0 else i for i in self.grid[x][y1:y2]]


    def read_coord(self, coord):
        return tuple(int(_) for _ in coord.split(","))


    def perform_instruction(self, instruction: str):
        # split instruction format
        # 0      1       2       3       4 
        # turn   off     60,313  through 75,728
        # turn   on      899,494 through 940,947
        # toggle 832,316 through 971,817
        
        instruction = instruction.split()
        if not instruction:
            return

        if instruction[0] == "toggle":
            x1,y1 = self.read_coord(instruction[1])
            x2,y2 = self.read_coord(instruction[3])
            if self.part == 1:
                self.toggle(x1, y1, x2, y2)
            else:
                self.make_brighter(x1, y1, x2, y2)
                self.make_brighter(x1, y1, x2, y2)
            return

        x1,y1 = self.read_coord(instruction[2])
        x2,y2 = self.read_coord(instruction[4])
        
        if self.part == 1:
            if instruction[1] == "on":
                self.turn_on(x1, y1, x2, y2)
            else:
                self.turn_off(x1,y1,x2,y2)
        else:
            if instruction[1] == "on":
                self.make_brighter(x1, y1, x2, y2)
            else:
                self.make_darker(x1,y1,x2,y2)


def part_one(puzzle_input):
    grid = LightGrid(1000)
    for instruction in puzzle_input:
        grid.perform_instruction(instruction)

    print(grid.count_lit())


def part_two(puzzle_input):
    grid = LightGrid(1000, 2)
    for instruction in puzzle_input:
        grid.perform_instruction(instruction)

    print(grid.count_lit())


if __name__ == "__main__":
    with open("day6.txt") as file:
        puzzle_input = file.readlines()

    part_one(puzzle_input)
    part_two(puzzle_input)

    