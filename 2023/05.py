from functions import *


class Almanach:
    """ Handles storing and range-based operations on entries. """
    def __init__(self):
        self.map_ = defaultdict(dict)

    def corresponds_to(self, source_: str, dest_: str, val_: int) -> int:
        """ Looks up the almanach to find the value of the destination corresponding to the source.
            If none found, correspondence is defined as the value of the source element. """
        if source_ not in self.map_:
            logging.error("The looked up source element \"{source_}\" is unknown.")
            exit(-1)
        elif dest_ not in self.map_[source_]:
            return val_
        # destination found for source, find if the requested value is somewhere
        for range_pair in self.map_[source_][dest_]:
            if range_pair[0][0] <= val_ <= range_pair[0][1]:
                offset = val_ - range_pair[0][0]
                return range_pair[1][0] + offset
        return val_

    def add_map(self, source_: str, dest_: str, s0_: int, d0_: int, rng_: int) -> None:
        if dest_ not in self.map_[source_]:
            self.map_[source_][dest_] = []
        self.map_[source_][dest_].append([[s0_, s0_+rng_-1], [d0_, d0_+rng_-1]])

    def find_seed_location(self, seed_number_: int) -> int:
        path = ["soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
        source = "seed"
        next_step = seed_number_
        for step in path:
            next_step = self.corresponds_to(source, step, next_step)
            source = step
        return next_step


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/05.in")

    almanach, line_i = Almanach(), 2
    while line_i < len(data):
        if data[line_i] == "":
            pass
        elif data[line_i][0].isalpha():
            source, destination = data[line_i].split("-")[0], data[line_i].split("-")[2].split()[0]
        elif data[line_i][0].isdecimal():
            dest_0, src_0, rng = list(map(int, data[line_i].split()))
            almanach.add_map(source, destination, src_0, dest_0, rng)
        line_i += 1

    seeds = list(map(int, data[0].split()[1:]))
    closest_location = float("inf")
    for seed in seeds:
        closest_location = min(closest_location, almanach.find_seed_location(seed))
    logging.info(f"Part 1: {closest_location=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
