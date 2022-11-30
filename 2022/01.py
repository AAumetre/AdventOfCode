from functions import *


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/01.ex")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
