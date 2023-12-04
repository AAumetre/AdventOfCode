from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/04.in")

    sum_points = 0
    card_copies = [1]*len(data)
    for index, line in enumerate(data):
        winning_numbers = set([int(n) for n in line.split(": ")[1].split(" | ")[0].split()])
        card_numbers = set([int(n) for n in line.split(": ")[1].split(" | ")[1].split()])
        c = len(winning_numbers.intersection(card_numbers))
        if c > 0:
            sum_points += pow(2, c-1)
            for i in range(1, c+1):
                card_copies[index+i] += card_copies[index]
    logging.info(f"Part 1: {sum_points=}")
    logging.info(f"Part 2: {sum(card_copies)=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
