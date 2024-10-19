from functions import *


def tilt_down(platform_: List[List]) -> List[List]:
    columns = [[line[i] for line in platform_] for i in range(len(platform_[0]))]
    empty_columns = [list(map(lambda s: "." if s == "O" else s, col)) for col in columns]
    col_height, total_load = len(columns[0]), 0
    for coli_, col in enumerate(columns):
        # find square rocks
        for pair_rocks in itertools.pairwise([i for i in range(len(col)) if col[i] == "#"]):
            # count round rocks in that range
            number_round_rocks = len(list(filter(lambda i: col[i] == "O", range(pair_rocks[0] + 1, pair_rocks[1]))))
            for i in range(number_round_rocks):
                empty_columns[coli_][pair_rocks[0]+i+1] = "O"  # place the round rock
                total_load += col_height - (pair_rocks[0] + i) - 2  # add up the load
    return [[col[i] for col in empty_columns] for i in range(len(empty_columns[0]))]  # transpose again


def north_load(platform_: List[List]) -> int:
    total_load, col_height = 0, len(platform_)
    for i, row in enumerate(platform_):
        total_load += (col_height - i - 1)*row.count("O")
    return total_load


def rotate(m_: List[List]) -> List[List]:
    return [[m_[j][i] for j in reversed(range(len(m_)))] for i in range(len(m_[0]))]


def cycle(platform):
    for i in range(4):
        platform = tilt_down(platform)
        platform = rotate(platform)
    return north_load(platform), platform


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/14.in")
    platform = ["#"*len(data[0])] + data + ["#"*len(data[0])]  # add one row of square rocks at the top and bottom
    for i, line in enumerate(platform):  # add one column of square rocks to the left and right
        platform[i] = "#" + line + "#"

    platform = tilt_down(platform)
    logging.info(f"Part 1: {north_load(platform)}")

    platform = [list(line) for line in platform]
    n_cycles = 1_000_000_000
    # find the period of the loads by auto-correlation
    loads, period, stopping_point, target_load_value = [], 0, -1, 0
    for i in range(n_cycles):
        load, platform = cycle(platform)
        if load in loads:
            if stopping_point == -1:
                # find index of the latest load occurrence, distance is assumed period T
                search_index = i-1
                while search_index >= 0:
                    if loads[search_index] == load:
                        break
                    search_index -= 1
                period = i - search_index
                stopping_point = i + period  # define stopping point as t+T
                if period == 1:
                    stopping_point = -1
            elif stopping_point == i:  # no mismatch so far, we validated the period
                target_load_value = loads[i - 1 - period + n_cycles%period - 1]
                break
            elif loads[i-period] != load:
                stopping_point = -1
        loads.append(load)

    logging.info(f"Part 2: {target_load_value}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
