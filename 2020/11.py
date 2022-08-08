import copy

from functions import *


def count_neighbors(seats: List[List[str]], i: int, j: int) -> int:
    neighbors = get_neighbor_indexes_euclidian(seats, i, j)
    count = 0
    for n in neighbors:
        if seats[n[1]][n[0]] == "#":
            count += 1
    return count

def is_inside(seats: List[List[str]], pos: List[int]) -> bool:
    if (not (0 <= pos[0] < len(seats[0]))) or (not (0 <= pos[1] < len(seats))):
        return False
    else:
        return True

def count_neighbors_direction(seats: List[List[str]], i: int, j: int) -> int:
    directions = [[-1,-1], [0,-1], [+1,-1],
                  [-1,0], [+1,0],
                  [-1,+1], [0,+1], [+1,+1]]
    count = 0
    for aim in directions:
        pos = [i+aim[0], j+aim[1]] # walk in that direction
        while is_inside(seats, pos):
            obj = seats[pos[1]][pos[0]]
            if obj == "#":
                count += 1
                break
            elif obj == "L":
                break
            else:
                pos = [pos[0]+aim[0], pos[1]+aim[1]] # walk in that direction
    return count


def fill_seats(seats: List[List[str]], max_occupied: int, counting: Callable) -> List[List[str]]:
    is_changing = True
    while is_changing:
        is_changing = False
        new_seats = copy.deepcopy(seats)
        for j in range(len(seats)):
            for i in range(len(seats[0])):
                seat = seats[j][i]
                if seat == ".": continue # skip if empty space
                nn = counting(seats, i, j)
                if seat == "L" and nn == 0:
                    is_changing = True
                    new_seats[j][i] = "#"
                elif seat == "#" and nn >= max_occupied:
                    is_changing = True
                    new_seats[j][i] = "L"
        seats = new_seats
    return seats

def count_occupied(seats: List[List[str]]) -> int:
    occupied_seats = 0
    for j in range(len(seats)):
        for i in range(len(seats[0])):
            if seats[j][i] == "#":
                occupied_seats += 1
    return occupied_seats

def main():
    logging.basicConfig(level=logging.DEBUG)
    seats = [list(line) for line in read_file("data/11.in")]

    seats_p1 = fill_seats(seats, 4, count_neighbors)
    logging.info(f"Part 1: there are {count_occupied(seats_p1)} occupied seats.")
    seats_p2 = fill_seats(seats, 5, count_neighbors_direction)
    logging.info(f"Part 2: there are {count_occupied(seats_p2)} occupied seats.")

main()