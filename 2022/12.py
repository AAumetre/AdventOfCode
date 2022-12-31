from functions import *

Position = Tuple[int, int]
Map = Dict[Position, int]
Path = List[Position]


def climb(from_: Position, to_: Position, map_: Map, width_: int, height_: int) -> Path:
    """ Finds the shortest path between two Positions and returns it (depth-first).
     Returns [] if no path can be found. """
    open_paths = collections.deque([[from_]])
    walked_through = set(from_)  # can be defined here, as we're using depth-first
    while open_paths:
        this_path = open_paths.popleft()  # depth-first
        i, j = this_path[-1]
        if (i, j) == to_:
            return this_path  # the first that is found is the shortest
        else:
            for ii, jj in (i + 1, j), (i, j - 1), (i - 1, j), (i, j + 1):
                if 0 <= ii < width_ and 0 <= jj < height_ and map_[(i, j)] + 1 >= map_[(ii, jj)]:
                    if (ii, jj) not in walked_through:  # prevent re-visit
                        open_paths.append(this_path + [(ii, jj)])
                        walked_through.add((ii, jj))  # the first that gets in is also the shortest
    return []


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/12.in")
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
    logging.info(f"The fewest number of steps to reach the location is {steps} steps.")

    fewest_steps = float("inf")
    for start in [pos for pos in terrain if terrain[pos] == ord("a")]:
        steps = -1 + len(climb(start, end_node, terrain, len(data[0]), len(data)))
        if 0 < steps < fewest_steps:
            fewest_steps = steps
    logging.info(f"The fewest steps required from any of the lowest points is {fewest_steps} steps.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")