from functions import *

spelled = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
           "nine": "9", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9"}


def parse_line(line_: str, digits_: List[str]) -> List[str]:
    for word, value in spelled.items():
        if line_.startswith(word):
            digits_.append(value)
    if len(line_) == 1:
        return digits_
    else:
        return parse_line(line_[1:], digits_)


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/01.in")

    sum_calibrations = 0
    for line in data:
        digits = list(filter(lambda x: x.isdecimal(), line))
        sum_calibrations += int(digits[0]+digits[-1])
    logging.info(f"Part 1: {sum_calibrations=}")

    sum_calibrations = 0
    for line in data:
        digits = parse_line(line, [])
        sum_calibrations += int(digits[0]+digits[-1])
    logging.info(f"Part 2: {sum_calibrations=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")