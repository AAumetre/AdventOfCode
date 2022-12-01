from functions import *


def main():
    logging.basicConfig(level=logging.DEBUG)
    calories = sorted([sum([int(i) for i in s.split(",")]) for s in ",".join(read_file("data/01.in")).split(",,")])
    logging.info(f"The maximum number of calories carried by an elf is {calories[-1]}.")
    logging.info(f"The sum of the three largest calorie-carrying elves is {sum(calories[-3:])}.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
