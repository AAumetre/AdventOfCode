from functions import *

Position = Tuple[int, int]


class Cavern:

    def __init__(self, rocks_: Set[Position]):
        self.filled_ = copy.deepcopy(rocks_)
        min_i, max_i = min([r[0] for r in rocks_]), max([r[0] for r in rocks_])
        min_j, max_j = 0, max([r[1] for r in rocks_])
        self.i_range_ = range(min_i, max_i + 1)
        self.j_range_ = range(min_j, max_j + 1)

    def __repr__(self):
        rep = ""
        for j in self.j_range_:
            for i in self.i_range_:
                if (i, j) in self.filled_:
                    rep += "#"
                else:
                    rep += "."
            rep += "\n"
        return rep


def drop_sand(cavern_: Cavern, limit_: bool = False) -> Tuple[bool, Cavern]:
    pos = (500, 0)
    can_move = True
    while can_move:
        can_move = False
        for new_position in (pos[0], pos[1]+1), (pos[0]-1, pos[1]+1), (pos[0]+1, pos[1]+1):
            if new_position not in cavern_.filled_:
                if new_position[1] not in cavern_.j_range_:
                    if limit_:
                        can_move = False
                        break
                    return False, cavern_
                can_move = True
                pos = new_position
                break
    cavern_.filled_.add(pos)
    return True, cavern_


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/14.in")

    scan = set()
    for line in data:
        for segment in itertools.pairwise([tuple(eval(p)) for p in line.split(" -> ")]):
            i_range = sorted([segment[0][0], segment[1][0]])
            j_range = sorted([segment[0][1], segment[1][1]])
            i_range[1] += 1
            j_range[1] += 1
            for point in itertools.product(range(*i_range), range(*j_range)):
                scan.add(point)
    cavern = Cavern(scan)
    logging.debug(f"\n{cavern}")

    success = True
    units = 0
    while success:
        success, cavern = drop_sand(cavern)
        units += success
    logging.debug(f"\n{cavern}")
    logging.info(f"{units} grains of sand can fall and stay somewhere.")

    cavern = Cavern(scan)
    max_j = list(cavern.j_range_)[-1] + 2
    cavern.j_range_ = range(0, max_j)
    cavern.i_range_ = range(500-max_j, 500+max_j)
    units = 0
    while (500, 0) not in cavern.filled_:
        success, cavern = drop_sand(cavern, True)
        units += success
    logging.debug(f"\n{cavern}")
    logging.info(f"{units} grains of sand can fall until the source is blocked.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
