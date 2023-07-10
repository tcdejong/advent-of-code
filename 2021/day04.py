from dataclasses import dataclass

def read_input():
    with open("day4.txt") as f:
        raw = f.readlines()

    numbers = [int(x) for x in raw[0].strip().split(',')]

    raw = raw[2:]

    num_boards = len(raw) // 6
    boards = [[line.split() for line in raw[i*6:i*6+5]] for i in range(num_boards)]
    boards = [[int(n) for row in x for n in row] for x in boards]

    boards = [BingoBoard(board) for board in boards]

    return numbers, boards


@dataclass
class BingoBoard:
    board: list[int]

    def __post_init__(self):
        assert len(self.board) == 25

    def get_rows(self) -> list[list[int]]:
        board = self.board
        return [board[row*5:row*5+5] for row in range(5)]

    def get_cols(self) -> list[list[int]]:
        return list(zip(*self.get_rows()))

    def has_won(self, seen) -> bool:
        rows = self.get_rows()
        cols = self.get_cols()
        lines = [*rows, *cols]        
        result = any(all(x in seen for x in line) for line in lines)
        return result

    def calc_score(self, seen, last_num):
        unmarked = sum(x for x in self.board if x not in seen)
        score = unmarked * last_num
        print(f'{unmarked=}, {score=}, {last_num=}')
        return score

    def wins_when(self, numbers):
        for i, num in enumerate(numbers):
            seen = numbers[:i]
            if self.has_won(seen):
                return i

    def __repr__(self) -> str:
        rows = self.get_rows()
        rows = ["\t".join(map(str, row)) for row in rows]
        rowstr = "\n".join(rows)
        return "\n".join(["==================================", rowstr, "=================================="])


def part_one():
    numbers, boards = read_input()
    seen = set(numbers[:5])

    for num in numbers[5:]:
        seen.add(num)

        for board in boards:
            if board.has_won(seen):
                return board.calc_score(seen, num)

    raise LookupError


def part_two():
    numbers, boards = read_input()
    last_winner = max(boards, key=lambda b: b.wins_when(numbers))
    seen = numbers[:last_winner.wins_when(numbers)]
    return last_winner.calc_score(seen, numbers[last_winner.wins_when(numbers)-1])



if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')



