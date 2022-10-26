from functions import *
from numpy import array

Position = Tuple[int,int]
Tiles = Dict[Position, bool]

movements = {"se": array([+1, -1]),
             "sw": array([-1, -1]),
             "ne": array([+1, +1]),
             "nw": array([-1, +1]),
             "e": array([+2, 0]),
             "w": array([-2, 0])}


def count_neighbors(tiles_: Tiles, this_tile_: Position) -> int:
    """ Counts the number of black tiles neighboring a given position. """
    count = 0
    for move in movements.values():
        if tiles_[tuple(array(this_tile_) + move)] is True:
            count += 1
    return count


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/24.ex")
    tiles = defaultdict(bool)
    for line in data:
        position = array([0, 0])
        # read the directions
        line_pt = 0
        while line_pt < len(line):
            if line_pt+2 <= len(line) and line[line_pt:line_pt+2] in movements:
                move = line[line_pt:line_pt+2]
                line_pt += 2
            else:
                move = line[line_pt:line_pt+1]
                line_pt += 1
            position += movements[move]
        tiles[tuple(position)] = (not tiles[tuple(position)])  # flip it
    black_tile_count = sum(tiles.values())
    logging.info(f"There are {black_tile_count} black tiles.")

    x_bounds = [0, 0]
    y_bounds = [0, 0]
    for pos, color in tiles.items(): # determin the space we need to check
        if color is True:
            x_bounds[0] = min(x_bounds[0], pos[0])
            x_bounds[1] = max(x_bounds[1], pos[0])
            y_bounds[0] = min(y_bounds[0], pos[1])
            y_bounds[1] = max(y_bounds[1], pos[1])
    days = 1
    while days <= 100:
        new_tiles = copy.deepcopy(tiles)
        new_bounds_x = x_bounds.copy()
        new_bounds_y = y_bounds.copy()
        for y in range(y_bounds[0]-1, y_bounds[1]+2):
            for x in range(x_bounds[0]-2, x_bounds[1]+3):
                n_black_neighbors = count_neighbors(tiles, (x, y))
                if tiles[(x, y)] is True and (n_black_neighbors == 0 or n_black_neighbors > 2):
                    new_tiles[(x, y)] = False
                    black_tile_count -= 1
                if tiles[(x, y)] is False and n_black_neighbors == 2:
                    new_tiles[(x, y)] = True
                    black_tile_count += 1
                    new_bounds_x[0] = min(new_bounds_x[0], x)
                    new_bounds_x[1] = max(new_bounds_x[1], x)
                    new_bounds_y[0] = min(new_bounds_y[0], y)
                    new_bounds_y[1] = max(new_bounds_y[1], y)
        tiles = new_tiles
        x_bounds = new_bounds_x
        y_bounds = new_bounds_y
        logging.debug(f"Day {days}: {black_tile_count} black tiles, {x_bounds=}, {y_bounds=}")
        days += 1
    logging.info(f"After 100 days, there are {black_tile_count} black tiles.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
