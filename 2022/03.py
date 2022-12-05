from functions import *


def priority(c_: str) -> int:
    """ Computes a character's priority. """
    upper_bonus = 0 if (c_ == c_.lower()) else 26
    return upper_bonus + 1 + ord(c_.lower()) - ord("a")


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/03.in")
    items_sum = 0
    for line in data:
        left_side, right_side = set(line[:len(line)//2]), set(line[len(line)//2:])
        items_sum += priority(left_side.intersection(right_side).pop())
    logging.info(f"The sum of priorities is {items_sum}.")

    badges_sum = 0
    i = 0
    while i < len(data):
        badges_sum += priority(set(data[i]).intersection(set(data[i+1])).intersection(set(data[i+2])).pop())
        i += 3
    logging.info(f"The sum of the badges priorities is {badges_sum}.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")