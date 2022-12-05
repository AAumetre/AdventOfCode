from functions import *

Stack = List[str]
Docks = Dict[int, Stack]


@dataclass()
class Move:
    qty_: int
    from_: int
    to_: int


def parse_stacks(line_: str, docks_: Docks) -> None:
    """ Reads a stack-line and updates the docks with the new crates. """
    index = 1
    while index < len(line_):
        stack_index = 1 + index // 4
        if line_[index] != " ":
            docks_[stack_index].append(line_[index])
        index += 4


def do_move(docks_: Docks, move_: Move, version_: int) -> None:
    """ Performs a move on the docks. """
    if version_ == 9000:
        picked_up = list(reversed(docks_[move_.from_][:move_.qty_]))
    else:
        picked_up = docks_[move_.from_][:move_.qty_]
    docks_[move_.from_] = docks_[move_.from_][move_.qty_:]
    docks_[move_.to_] = picked_up + docks_[move_.to_]


def read_top_stacks(docks_: Docks) -> str:
    """ Reads the top of each stack and returns the corresponding string. """
    top_stacks = ""
    for i in range(1, 1+len(docks_)):
        if docks_[i]:
            top_stacks += docks_[i][0]
    return top_stacks


def main():
    logging.basicConfig(level=logging.DEBUG)
    docks: Docks = defaultdict(list)
    moves: List[Move] = []
    filename = "data/05.in"
    with open(filename, 'r') as f:
        for line in f:
            if "[" in line:
                parse_stacks(line, docks)
            elif line[0] == "m":
                split_line = line.split()
                moves.append(Move(int(split_line[1]), int(split_line[3]), int(split_line[5])))
    same_docks = copy.deepcopy(docks)
    # simulate the moves with CrateMover 9000
    for move in moves:
        do_move(docks, move, 9000)
    logging.info(f"The crates at the top of the stack are \"{read_top_stacks(docks)}\".")
    # simulate the moves with CrateMover 9001
    for move in moves:
        do_move(same_docks, move, 9001)
    logging.info(f"The crates at the top of the stack are \"{read_top_stacks(same_docks)}\".")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")