from functions import *


def transform(in_: int, subject_: int, loop_size_: int) -> int:
    val = in_
    for _ in range(loop_size_):
        val *= subject_
        val = val % 20201227
    return val


def find_loop_size(public_key_: int) -> int:
    loop_size = 0
    key = 1
    while key != public_key_:
        loop_size += 1
        key = transform(key, 7, 1)
    return loop_size


def main():
    logging.basicConfig(level=logging.DEBUG)
    card_public_key = 5764801
    door_public_key = 17807724
    card_public_key = 16915772
    door_public_key = 18447943
    card_loop_size = find_loop_size(card_public_key)
    door_loop_size = find_loop_size(door_public_key)
    logging.debug(f"{card_loop_size=}, {door_loop_size=}")

    encryption_key = transform(1, door_public_key, card_loop_size)
    logging.info(f"The encryption key is {encryption_key}.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")