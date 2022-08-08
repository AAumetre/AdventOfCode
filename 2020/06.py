import string

from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/06.ex")
    data.append("")
    group_answers = defaultdict(int)
    sum = 0
    participants = 0
    unanimous_sum = 0
    for line in data:
        if line == "":
            for letter, count in group_answers.items():
                sum += 1
                if count == participants:
                    unanimous_sum += 1
            group_answers = defaultdict(int)
            participants = 0
        else:
            for letter in line:
                group_answers[letter] += 1
            participants += 1
    logging.info(f"Part 1: {sum} answers")
    logging.info(f"Part 2: {unanimous_sum} unanimous answers")

main()