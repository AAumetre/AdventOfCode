from functions import *
import bisect


def main():
    data = read_file("data/01.in")

    left, right = map(sorted, zip(*[map(int, line.split()) for line in data]))
    logging.info(f"Part 1: {sum([abs(l-r) for l, r in zip(left, right)])}")
    logging.info(f"Part 2: {reduce(lambda x, y: x+y*right.count(y), left, 0)}")


logging.basicConfig(level=logging.INFO)
start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
