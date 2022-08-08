from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    seats = read_file("data/05.in")
    highest_id = 0
    seat_ids = {}
    for seat in seats:
        row = int(seat[:7].replace("B", "1").replace("F", "0"), 2)
        col = int(seat[7:].replace("R", "1").replace("L", "0"), 2)
        id = row*8+col
        seat_ids[id] = True
        highest_id = max(highest_id, id)
    logging.info(f"Part 1: largest ID is {highest_id}")
    for i in range(1, highest_id-1):
        if i not in seat_ids:
            if i-1 in seat_ids and i+1in seat_ids:
                logging.info(f"Part 2: your ID is {i}")
                break

main()