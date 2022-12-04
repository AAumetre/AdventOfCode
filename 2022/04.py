from functions import *


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/04.in")

    contained_ranges = 0
    range_overlaps = 0
    for line in data:
        left_bounds = list(map(lambda x: int(x), line.split(",")[0].split("-")))
        right_bounds = list(map(lambda x: int(x), line.split(",")[1].split("-")))
        left_set = set(list(range(left_bounds[0], left_bounds[1]+1)))
        right_set = set(list(range(right_bounds[0], right_bounds[1]+1)))
        new_intersection = list(left_set.intersection(right_set))
        if new_intersection == list(left_set) or new_intersection == list(right_set):
            contained_ranges += 1
        if new_intersection != []:
            range_overlaps += 1
    logging.info(f"There are {contained_ranges} that completely overlap.")
    logging.info(f"There are {range_overlaps} that overlap.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")