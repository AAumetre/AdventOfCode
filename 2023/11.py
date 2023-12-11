from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/11.ex")

    unexpanded_space = set()
    columns_to_expand = set(range(len(data[0])))
    lines_to_expand = []
    for index, line in enumerate(data):
        galaxies = [i for i, v in enumerate(line) if v == "#"]
        if len(galaxies) == 0:
            lines_to_expand.append(index)
        else:
            unexpanded_space |= set(zip(galaxies, [index] * len(galaxies)))  # note their positions
            columns_to_expand = columns_to_expand.difference(set(galaxies))
    # expand space
    col_expanded_space = set()
    for galaxy in unexpanded_space:
        col_expanded_space.add((galaxy[0] + len(list(filter(lambda x: x < galaxy[0], columns_to_expand))),
                                galaxy[1]))
    space = set()
    for galaxy in col_expanded_space:
        space.add((galaxy[0],
                   galaxy[1] + len(list(filter(lambda x: x < galaxy[1], lines_to_expand)))))
    print(space)


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
