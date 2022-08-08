from dataclasses import dataclass
from functions import *


def solve(starting_numbers: List[int], position: int) -> int:
    game_log = defaultdict(int)
    game_turn = 1
    # initialisation phase
    for n in starting_numbers:
        game_log[n] = game_turn
        game_turn += 1
    delta = 0 # it's assumed the input is made of new numbers only
    while game_turn != position:
        new_number = delta
        if delta == 0:  # means it's new
            delta = game_turn - game_log[new_number]
        else:
            if new_number in game_log:
                delta = game_turn - game_log[new_number]
            else:
                delta = 0
        game_log[new_number] = game_turn
        game_turn += 1
        logging.debug(f"{game_turn}: {new_number=}")
    return delta

def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/15.in")
    starting_numbers = [int(e) for e in data[0].split(",")]
    logging.info(f"{starting_numbers=}")

    logging.info(f"The 2020th number is {solve(starting_numbers, 2020)}")
    logging.info(f"The 30000000th number is {solve(starting_numbers, 30000000)}")

main()