from functions import *

Position = Tuple[int, int]


class Cavern:

    def __init__(self, rocks_: Set[Tuple]):
        self.filled_ = copy.deepcopy(rocks_)
        mi, Mi = min([r[0] for r in rocks_]), max([r[0] for r in rocks_])
        mj, Mj = min([r[1] for r in rocks_]), max([r[1] for r in rocks_])
        self.i_range_ = range(mi, Mi + 1)
        self.j_range_ = range(mj, Mj + 1)
        self.top_left_ = (mi, mj)

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


def drop_sand(cavern_: Cavern) -> Tuple[bool, Cavern]:
    position = (500, 1)
    can_move = True
    while can_move:
        can_move = False
        for new_position in (position[0], position[1]+1), (position[0]-1, position[1]+1), (position[0]+1, position[1]+1):
            if new_position not in cavern_.filled_:
                can_move = True
                if new_position[0] not in cavern_.i_range_ or new_position[1] not in cavern_.j_range_:
                    return False, cavern_
                position = new_position
                break
            else:
                can_move = False
    cavern_.filled_.add(position)
    return True, cavern_


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/14.ex")

    scan = {(500, 0)}
    for line in data:
        for segment in itertools.pairwise([tuple(eval(p)) for p in line.split((" -> "))]):
            i_range = sorted([segment[0][0], segment[1][0]])
            j_range = sorted([segment[0][1], segment[1][1]])
            i_range[1] += 1
            j_range[1] += 1
            for point in itertools.product(range(*i_range), range(*j_range)):
                scan.add(point)
    cavern = Cavern(scan)
    print(cavern)

    success = True
    units = 0
    while success:
        success, cavern = drop_sand(cavern)
        print("=============================================")
        print(cavern)
        units += success
    logging.info(f"{units} grains of sand can fall and stay somewhere.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
