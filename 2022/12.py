from functions import *

Position = Tuple[int, int]
Map = Dict[Position, int]
Path = List[Position]


def climb(from_: Position, to_: Position, map_: Map, width_: int, height_: int) -> Path:
    """ Finds the shortest path between two Positions and returns it (breadth-first). """
    open_paths = collections.deque([[from_]])
    best_path = [float("inf"), []]
    seen = set()
    while open_paths:
        this_path = open_paths.pop()
        i, j = this_path[-1]
        if (i, j) == to_ and len(this_path) < best_path[0]:
            best_path = [len(this_path), this_path]
        else:
            for di, dj in (1, 0), (0, -1), (-1, 0), (0, 1):
                ii, jj = i + di, j + dj
                if 0 <= ii < width_ and 0 <= jj < height_ and map_[(i, j)] + 1 >= map_[(ii, jj)]:
                    if (ii,jj) not in this_path:  # prevent re-visit
                        open_paths.append(this_path + [(ii, jj)])
    return best_path[1]


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/12.ex")
    terrain = defaultdict(int)
    for j, line in enumerate(data):
        for i, c in enumerate(line):
            if c == "S":
                terrain[(i, j)] = ord("a")
                start_node = (i, j)
            elif c == "E":
                terrain[(i, j)] = ord("z")
                end_node = (i, j)
            else:
                terrain[(i, j)] = ord(c)
    steps = -1 + len(climb(start_node, end_node, terrain, len(data[0]), len(data)))
    logging.info(f"The fewest number of steps to reach the location is {steps}.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")