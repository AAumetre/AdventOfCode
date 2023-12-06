from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/06.in")

    races = list(zip(list(map(int, data[0].split()[1:])), list(map(int, data[1].split()[1:]))))
    total_number_ways_to_win = 1
    for race in races:
        number_ways_to_win = 0
        for speed in range(1, race[0]):  # ignore 0 ms of holding and full holding
            if (race[0] - speed) * speed > race[1]:  # speed is also the holding duration
                number_ways_to_win += 1
        total_number_ways_to_win *= number_ways_to_win
    logging.info(f"Part 1: {total_number_ways_to_win=}")

    race = [int(data[0].replace(" ", "").split(":")[1]), int(data[1].replace(" ", "").split(":")[1])]
    number_ways_to_win = 0
    for speed in range(1, race[0]):  # ignore 0 ms of holding and full holding
        if (race[0] - speed) * speed > race[1]:  # speed is also the holding duration
            number_ways_to_win += 1
    logging.info(f"Part 2 {number_ways_to_win=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
