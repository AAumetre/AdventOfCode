from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/02.in")

    sum_ids = 0
    sum_powers = 0
    for line in data:
        color_picks = [[s.split(" ") for s in r.split(", ")] for r in line.split(": ")[1].split("; ")]
        tuple_rounds = []
        for a_round in color_picks:
            list_round = [0, 0, 0]
            for pick in a_round:
                if pick[1] == "red":
                    list_round[0] += int(pick[0])
                elif pick[1] == "green":
                    list_round[1] += int(pick[0])
                else:
                    list_round[2] += int(pick[0])
            tuple_rounds.append(tuple(list_round))
        if all(map(lambda t: t[0] < 13 and t[1] < 14 and t[2] < 15, tuple_rounds)):
            sum_ids += int(line.split(" ")[1][:-1])
        sum_powers += reduce(operator.mul, [max(c) for c in list(zip(*tuple_rounds))])
    logging.info(f"Part 1: {sum_ids=}")
    logging.info(f"Part 2: {sum_powers=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
