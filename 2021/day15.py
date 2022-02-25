from dataclasses import dataclass

Position = tuple[int, int]

def read_input(use_example = False):
    filename = 'day15ex.txt' if use_example else 'day15.txt'
    with open(filename) as f:
        raw = [list(int(i) for i in line.strip()) for line in f.readlines() if line]

    cavemap = {(x,y): risk for y, line in enumerate(raw) for x, risk in enumerate(line)}
    return cavemap


def part_one(use_example):
    cavemap = read_input(use_example)
    navi = CaveNavigator(cavemap)
    return navi.navigate()


def part_two(use_example):
    cavemap = read_input(use_example)
    new_map = update_cavemap(cavemap)
    navi = CaveNavigator(new_map)
    return navi.navigate()


def update_cavemap(cavemap: dict[Position: int]):
    # For each point generate 4 points repeated on x
    # For the 5 points on x, generated 5 copies on y

    new_map = {}

    exit_node = list(cavemap.keys())[-1]
    dx, dy = exit_node
    dx, dy = dx + 1, dy + 1 # offset to avoid overlap

    repetitions = 5

    for rx in range(repetitions):
        for ry in range(repetitions):
            for (x,y),risk in cavemap.items():
                # print(x,y,risk)
                new_pos = (x + rx*dx, y + ry*dy)
                new_risk = (risk + rx + ry) % 9
                new_risk = 9 if new_risk == 0 else new_risk
                new_map[new_pos] = new_risk

    return new_map


@dataclass
class CaveNavigator:
    cavemap: dict[Position: int]

    def __post_init__(self):
        self.start_node: Position = (0,0)
        self.exit_node = list(self.cavemap.keys())[-1]
        self.heur_weight = 1

        # G-cost: distance from start
        # H-cost: assumed distance to end
        # F-cost: G-cost + H-cost

        self.g_costs = {self.start_node: 0}
        self.h_costs = {}
        self.get_h_cost(self.start_node)

        self.open_nodes: set(Position) = {self.start_node}
        self.seen_nodes: set(Position) = set()
        self.arrive_from: dict[Position: Position] = {self.start_node: self.start_node}


    def get_f_cost(self, node: Position):
        return self.g_costs.get(node, self.h_costs[self.start_node]) + self.get_h_cost(node)


    def get_h_cost(self, pos: Position):
        if pos in self.h_costs:
            return self.h_costs[pos]

        px, py = pos
        exit_node = list(self.cavemap.keys())[-1]
        ex, ey = exit_node
        
        dx = abs(ex - px)
        dy = abs(ey - py)

        hcost = (dx + dy) * self.heur_weight

        self.h_costs[pos] = hcost

        return hcost


    def navigate(self, step_once = False):
        while self.exit_node not in self.seen_nodes:
            next_node = self.select_next()
            self.visit_node(next_node)

            if step_once:
                return

        return self.total_path_cost(self.exit_node)

    
    def visit_node(self, node):
        self.seen_nodes.add(node)
        self.open_nodes = self.open_nodes - self.seen_nodes
        open_nbs = self.get_nbs(node) - self.seen_nodes

        self.update_open_nodes(open_nbs, node)

        self.open_nodes = self.open_nodes | open_nbs


    def select_next(self):
        if len(self.open_nodes) == 1:
            return self.open_nodes.pop()

        next_node = min(self.open_nodes, key=lambda x: self.get_f_cost(x))

        if not next_node:
            raise ValueError("Next node is falsey!")

        return next_node
        

    def update_open_nodes(self, nodes, visited_node):
        for open_node in nodes:  

            new_gcost = self.g_costs[visited_node] + self.cavemap[open_node]

            if open_node not in self.g_costs or new_gcost < self.g_costs[open_node]:
                self.g_costs[open_node] = new_gcost
                self.arrive_from[open_node] = visited_node


    def total_path_cost(self, node: Position):
        return self.g_costs[node]


    def get_nbs(self, pos: Position) -> set[Position]:
        x,y = pos
        
        minx, miny = 0, 0
        maxx, maxy = self.exit_node

        up = (x, y-1) if y > miny else None
        down = (x, y+1) if y < maxy else None
        left = (x-1, y) if x > minx else None
        right = (x+1, y) if x < maxx else None

        nbs = set(pos for pos in [up, down, left, right] if pos != None)

        return nbs


def print_cavemap(cavemap):
    last = list(cavemap.keys())[-1]
    w, h = last
    w, h = w+1, h+1

    lines = ["".join(str(cavemap[(x,y)]) for x in range(w)) for y in range(h)]
    
    [print(line) for line in lines]
    

if __name__ == '__main__':
    assert part_one(True) == 40
    assert part_two(True) == 315
    
    USE_EX = False
    print(f'Part one: {part_one(USE_EX)}')
    print(f'Part two: {part_two(USE_EX)}')



