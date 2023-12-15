from functions import *


Position = Tuple[int, int]


def expand_space(unexpanded_space, columns_to_expand, lines_to_expand, expansion) -> List[Position]:
    col_expanded_space = []
    for galaxy in unexpanded_space:
        col_expanded_space.append((galaxy[0] + (expansion-1)*len(list(filter(lambda x: x < galaxy[0], columns_to_expand))),
                                   galaxy[1]))
    space = []
    for galaxy in col_expanded_space:
        space.append((galaxy[0],
                      galaxy[1] + (expansion-1)*len(list(filter(lambda x: x < galaxy[1], lines_to_expand)))))
    return space


def get_sum_distances(space):
    sum_shortest_path = 0
    for i, galaxy in enumerate(space[:-1]):
        for j, other in enumerate(space[i + 1:]):
            sum_shortest_path += abs(galaxy[0] - other[0]) + abs(galaxy[1] - other[1])
    return sum_shortest_path


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/11.in")

    # read input
    unexpanded_space = []
    columns_to_expand = set(range(len(data[0])))
    lines_to_expand = []
    for index, line in enumerate(data):
        galaxies = [i for i, v in enumerate(line) if v == "#"]
        if len(galaxies) == 0:
            lines_to_expand.append(index)
        else:
            unexpanded_space += list(zip(galaxies, [index] * len(galaxies)))  # note their positions
            columns_to_expand = columns_to_expand.difference(set(galaxies))

    sum_shortest_path = get_sum_distances(
        expand_space(unexpanded_space, columns_to_expand, lines_to_expand, 2))
    logging.info(f"Part 1: {sum_shortest_path=}")

    sum_shortest_path = get_sum_distances(
        expand_space(unexpanded_space, columns_to_expand, lines_to_expand, 1_000_000))
    logging.info(f"Part 2: {sum_shortest_path=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
