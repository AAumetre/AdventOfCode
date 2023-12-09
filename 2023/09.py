from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/09.in")

    sum_extrapolated_values_right, sum_extrapolated_values_left = 0, 0
    for line in data:
        history = [list(map(int, line.split()))]
        while not all(map(lambda x: x == 0, history[-1])):
            history.append([history[-1][i+1]-history[-1][i] for i in range(len(history[-1])-1)])
        history[-1].append(0)
        for i in reversed(range(len(history)-1)):
            history[i].append(history[i+1][-1] + history[i][-1])
        sum_extrapolated_values_right += history[0][-1]
        history[-1].append(0)
        for i in reversed(range(len(history)-1)):
            history[i].append(history[i][0] - history[i+1][-1])
        sum_extrapolated_values_left += history[0][-1]
    logging.info(f"Part 1: {sum_extrapolated_values_right=}")
    logging.info(f"Part 1: {sum_extrapolated_values_left=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
