from functions import *


def is_safe(line_: List[int]) -> bool:
    deltas = [x - y for x, y in zip(line_[:-1], line_[1:])]
    return  all(map(lambda e: e in [1, 2, 3], deltas)) or all(map(lambda e: e in [-1, -2, -3], deltas))


def main():
    data = [list(map(int, e.split())) for e in read_file("data/02.in")]
    logging.info(f"Part 1: {sum(map(is_safe, data))}")
    logging.info(f"Part 2: {sum([any(map(is_safe, [line[:i]+line[i+1:] for i in range(len(line))])) for line in data])}")


logging.basicConfig(level=logging.INFO)
start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
