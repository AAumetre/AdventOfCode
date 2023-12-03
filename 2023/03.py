from functions import *

Position = Tuple[int, int]


@dataclass
class Number:
    val_: int
    zone_: Set[Position]


def surroundings(i: int, j: int) -> Set[Position]:
    return {(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1),
            (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)}


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/03.in")

    # first, do a scan of symbols' and gears' positions
    symbols_zones = set()
    gears = {}
    gears_zones = set()
    for j in range(len(data)):
        for i in range(len(data[0])):
            if not data[j][i].isdecimal() and data[j][i] != ".":
                symbols_zones |= surroundings(i, j)
            if data[j][i] == "*":
                this_gear_zone = surroundings(i, j)
                gears_zones |= this_gear_zone
                gears[tuple(this_gear_zone)] = {"pos": (i, j), "parts": []}
    # then, do a scan of numbers, taking into account exclusion zones
    sum_part_numbers = 0
    numbers = []
    for j in range(len(data)):
        i = 0
        while i < len(data[0]):
            if data[j][i].isdecimal():
                i_values = []
                while i < len(data[0]) and data[j][i].isdecimal():
                    i_values.append(i)
                    i += 1
                # need to compute the position of every digit of e
                digits_positions = set(zip(i_values, [j] * len(i_values)))
                numbers.append(Number(int(data[j][i_values[0]:i_values[-1] + 1]), digits_positions))
                if symbols_zones.intersection(digits_positions):
                    sum_part_numbers += numbers[-1].val_
            i += 1
    logging.info(f"Part 1: {sum_part_numbers=}")

    # find numbers that are close to gears
    sum_gear_ratios = 0
    for number in numbers:
        if gears_zones.intersection(number.zone_):
            for gear_zone, gear_info in gears.items():
                if set(gear_zone).intersection(number.zone_):
                    gear_info["parts"].append(number.val_)
    # now, let's look at gears that move only two parts
    for gear_zone, gear_info in gears.items():
        if len(gear_info["parts"]) == 2:
            sum_gear_ratios += gear_info["parts"][0] * gear_info["parts"][1]
    logging.info(f"Part 2: {sum_gear_ratios=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
