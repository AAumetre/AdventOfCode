from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/04.in")

    sum_points = 0
    for line in data:
        winning_numbers = set([int(n) for n in line.split(": ")[1].split(" | ")[0].split()])
        card_numbers = set([int(n) for n in line.split(": ")[1].split(" | ")[1].split()])
        c = len(winning_numbers.intersection(card_numbers))
        if c > 0:
            sum_points += pow(2, c-1)
    logging.info(f"Part 1: {sum_points=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
