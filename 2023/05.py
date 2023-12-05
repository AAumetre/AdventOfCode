from functions import *

path = ["soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]


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

    ranges = [[e[0], e[0]+e[1]-1] for e in list(zip(seeds[::2], seeds[1::2]))]
    spath = ["seed"] + path
    step_i = 0
    while step_i < len(spath)-1:
        mapped_ranges = []
        for mapping in almanach.map_[spath[step_i]][spath[step_i+1]]:
            for current_range in ranges:
                # find the intersection of a current range with the source range of the current mapping
                inter = [max(current_range[0], mapping[0][0]), min(current_range[1], mapping[0][1])]
                if inter[1] >= inter[0]:  # intersection exists
                    mapped_ranges.append(inter)
        # find parts of the ranges which are not mapped (kept as-is)
        unmapped_ranges = ranges.copy()
        # subtract all the mapped ranges from current ranges
        for mapped_range in mapped_ranges:
            new_unmapped_ranges = []
            to_delete = []
            for current_range in unmapped_ranges:
                # remove mapped_range from current_range, if any intersection
                inter = [max(current_range[0], mapped_range[0]), min(current_range[1], mapped_range[1])]
                if inter[1] >= inter[0]:  # intersection exists
                    to_delete = current_range
                    if inter == current_range:  # completely mapped
                        pass
                    elif inter[0] == current_range[0]:  # contains left part
                        new_unmapped_ranges.append([inter[1]+1, current_range[1]])
                    elif inter[1] == current_range[1]:  # contains right part
                        new_unmapped_ranges.append([current_range[0], inter[0]-1])
                    else:  # intersection is inside the current range
                        new_unmapped_ranges.append([current_range[0], inter[0]-1])
                        new_unmapped_ranges.append([inter[1]+1, current_range[1]])
                    continue
            unmapped_ranges.remove(to_delete)
            unmapped_ranges += new_unmapped_ranges
        # now, update the new ranges, with the mapping of mapped ranges and the unmapped ranges
        ranges = unmapped_ranges
        for range_to_map in mapped_ranges:
            mapped_range = []
            for mapping in almanach.map_[spath[step_i]][spath[step_i + 1]]:
                if mapping[0][0] <= range_to_map[0] <= mapping[0][1]:
                    offset = mapping[1][0]-mapping[0][0]
                    mapped_range = [range_to_map[0]+offset, range_to_map[1]+offset]
                    continue
            ranges.append(mapped_range)
        step_i += 1

    closest_location = min(itertools.chain.from_iterable(ranges))
    logging.info(f"Part 2: {closest_location=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
