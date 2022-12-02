from functions import *


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/02.in")
    scores = {"A X": 4, "A Y": 8, "A Z": 3,
              "B X": 1, "B Y": 5, "B Z": 9,
              "C X": 7, "C Y": 2, "C Z": 6}
    logging.info(f"The score according to the strategy is {sum(map(lambda x: scores[x], data))}.")
    scores = {"A X": 3, "A Y": 4, "A Z": 8,
              "B X": 1, "B Y": 5, "B Z": 9,
              "C X": 2, "C Y": 6, "C Z": 7}
    logging.info(f"The score according to the other strategy is {sum(map(lambda x: scores[x], data))}.")

start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
