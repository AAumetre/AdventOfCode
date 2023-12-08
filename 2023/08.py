from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/08.in")

    directions = [0 if d == "L" else 1 for d in data[0]]
    nodes = {}
    for line in data[2:]:
        nodes[line.split(" = ")[0]] = line[:-1].split(" = (")[1].split(", ")
    pos, steps, reached = "AAA", 0, False
    while not reached:
        pos = nodes[pos][directions[steps%len(directions)]]
        steps += 1
        if pos == "ZZZ":
            reached = True
    logging.info(f"Part 1: {steps=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
