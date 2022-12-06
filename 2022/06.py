from functions import *


def detect_marker(line_: str, size_: int) -> int:
    """ Detects a size_ of unique characters and returns the
    number of characters to be processed. """
    for i in range(len(line_)-size_):
        marker_chars = set(line_[i:i+size_])
        if len(marker_chars) == size_:
            return i+size_
    return 0


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/06.in")
    line = data[0]
    logging.info(f"The start-of-packet appears after {detect_marker(line, 4)} characters.")
    logging.info(f"The start-of-message appears after {detect_marker(line, 14)} characters.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")