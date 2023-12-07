from functions import *


def hand_type(hand_: List[int]) -> int:
    count = defaultdict(int)
    for card in hand_:
        count[card] += 1
    counts = list(count.values())
    if max(counts) == 1:
        return 1  # high card
    if counts.count(2) == 1 and counts.count(3) == 0:
        return 2  # one pair
    if counts.count(2) == 2:
        return 3  # two pairs
    if counts.count(3) == 1 and counts.count(2) == 0:
        return 4  # three of a kind
    if counts.count(3) == 1 and counts.count(2) == 1:
        return 5  # full house
    if counts.count(4) == 1:
        return 6  # four of a kind
    if counts.count(5) == 1:
        return 7  # five of a kind


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/07.in")

    powers = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "T": 8,
              "J": 9, "Q": 10, "K": 11, "A": 12}
    hands = []
    for line in data:
        cards = list(map(lambda x: powers[x], line.split()[0]))
        power = int("".join([str(e).zfill(2) for e in [hand_type(cards)] + cards]))
        hands.append((power, int(line.split()[1])))
    hands = sorted(hands, key=lambda x: x[0])
    total_winnings = sum([(index+1)*hand[1] for index, hand in enumerate(hands)])
    logging.info(f"Part 1: {total_winnings=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
