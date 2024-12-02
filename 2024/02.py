from functions import *


def is_safe(line_: List[int]) -> bool:
    up = all(map(lambda e: e in [1, 2, 3], [x - y for x, y in zip(line_[:-1], line_[1:])]))
    do = all(map(lambda e: e in [-1, -2, -3], [x - y for x, y in zip(line_[:-1], line_[1:])]))
    return up or do


def main():
    data = read_file("data/02.in")

    count = sum(map(is_safe, [list(map(int, e.split())) for e in data]))
    logging.info(f"Part 1: {count}")
    count = sum([any(map(is_safe, [line[:i]+line[i+1:] for i in range(len(line))])) for line in [list(map(int, e.split())) for e in data]])
    logging.info(f"Part 2: {count}")


logging.basicConfig(level=logging.INFO)
start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
