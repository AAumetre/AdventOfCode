from functions import *

Position = Tuple[int, int]  # x, y


class Point:
    def __init__(self, pos_: Position, symbol_: str):
        self.pos_: Position = pos_
        n = {"F": [(1, 0), (0, 1)], "7": [(-1, 0), (0, 1)], "J": [(0, -1), (-1, 0)], "L": [(0, -1), (1, 0)],
             "|": [(0, -1), (0, 1)], "-": [(-1, 0), (1, 0)], ".": [], "S": [(0, -1), (0, 1), (-1, 0), (1, 0)]}
        self.symbol_ = symbol_
        self.neighbors_: List[Position] = [(pos_[0] + dx, pos_[1] + dy) for dx, dy in n[symbol_]]

    def __repr__(self):
        return f"{self.symbol_}@{self.pos_}"


@dataclass()
class Path:
    points_: List[Point]

    def add_point(self, point_: Point) -> Self:
        """ Creates a new path from self and a new point. """
        return Path(self.points_ + [point_])  # shallow copy is enough, nobody touches Point


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/10.in")

    for index, line in enumerate(data):  # look for the starting position
        if "S" in line:
            s_pos = (line.find("S"), index)
            break

    open_paths = [Path([Point(s_pos, "S")])]
    while open_paths:
        a_path = open_paths.pop()
        last_point = a_path.points_[-1]
        for n_pos in filter(lambda p: 0 <= p[1] <= len(data) and 0 <= p[0] <= len(data[0]), last_point.neighbors_):
            n_point = Point(n_pos, data[n_pos[1]][n_pos[0]])
            if last_point.pos_ not in set(n_point.neighbors_):  # check if neighbor is unreachable
                continue
            elif len(a_path.points_) > 2 and n_pos == a_path.points_[-2].pos_:  # prevent backtracking
                continue
            elif n_pos == s_pos and len(a_path.points_) > 2:  # stop here, the other one is the same, in reverse
                big_loop = a_path
                open_paths = []
                break
            else:
                open_paths.append(a_path.add_point(n_point))
    logging.info(f"Part 1: {len(big_loop.points_)//2=}")

    # use shoelace formula to compute the polygon's surface area (https://en.wikipedia.org/wiki/Shoelace_formula)
    loop_area = 0
    for k, point in enumerate(big_loop.points_):
        x_prev = big_loop.points_[k - 1].pos_[0]
        x_next = big_loop.points_[k + 1].pos_[0] if k < len(big_loop.points_) - 1 else big_loop.points_[0].pos_[0]
        loop_area += point.pos_[1] * (x_prev - x_next)
    loop_area = abs(loop_area // 2)  # depending on the direction, might be negative
    enclosed_tiles = loop_area - len(big_loop.points_) // 2 + 1
    logging.info(f"Part 2: {enclosed_tiles=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
