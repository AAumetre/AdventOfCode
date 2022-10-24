from functions import *
from numpy import array


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/24.in")

    movements = {"se": array([+1, -1]),
                 "sw": array([-1, -1]),
                 "ne": array([+1, +1]),
                 "nw": array([-1, +1]),
                 "s":  array([0, -2]),
                 "n":  array([0, +2]),
                 "e":  array([+2, 0]),
                 "w":  array([-2, 0])}

    tiles = defaultdict(lambda: False)
    for line in data:
        position = array([0, 0])
        # read the directions
        line_pt = 0
        while line_pt < len(line):
            if line_pt+2 <= len(line) and line[line_pt:line_pt+2] in movements:
                move = line[line_pt:line_pt+2]
                line_pt += 2
            else:
                move = line[line_pt:line_pt+1]
                line_pt += 1
            position += movements[move]
            logging.debug(f"The move is {move}.")
        tiles[tuple(position)] = (not tiles[tuple(position)])  # flip it
    logging.info(f"There are {sum(tiles.values())} black tiles.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
