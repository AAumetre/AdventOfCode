from functions import *

Position = Tuple[int, int]
Map = Dict[int, List[bool]]

@dataclass()
class Shape:
    points_: List[Position]
    height_: int
    width_: int


def next_circular_index(index_: int, size_: int) -> int:
    if index_ + 1 > size_ - 1: return 0
    return index_ + 1

def can_move_there(target_: Position, shape_: Shape, chamber_: Map) -> bool:
    for point in [(target_[0]+offset[0], target_[1]-offset[1]) for offset in shape_.points_]:
        if point[0] < 0 or point[0] > 6 or point[1] < 1:
            return False
        if point[1] in chamber_ and chamber_[point[1]][point[0]]:
            return False
    return True

def add_stone_to_map(shape_: Shape, position_: Position, chamber_: Map) -> None:
    for point in [(position_[0]+offset[0], position_[1]-offset[1]) for offset in shape_.points_]:
        chamber_[point[1]][point[0]] = True

def let_rocks_fall(shapes_: List[Shape], jets_: str, count_: int) -> int:
    highest_point = 0
    fallen_rocks = 0
    shape_index = 0
    shape = shapes_[shape_index]
    jet_index = 0
    chamber: Map = defaultdict(lambda: [False] * 7)

    while fallen_rocks < count_:
        position = (2, highest_point + 3 + shape.height_)
        has_stopped = False
        is_jet_turn = True
        while not has_stopped:
            if is_jet_turn:
                new_position = (position[0] - 1, position[1]) if jets_[jet_index] == "<" else (
                position[0] + 1, position[1])
                if can_move_there(new_position, shape, chamber):
                    position = new_position
                jet_index = next_circular_index(jet_index, len(jets_))
            else:
                new_position = (position[0], position[1] - 1)
                if can_move_there(new_position, shape, chamber):
                    position = new_position
                else:
                    has_stopped = True
            is_jet_turn = not is_jet_turn
        # now add the stone to the chamber map and update the highest point
        add_stone_to_map(shape, position, chamber)
        highest_point = max(highest_point, position[1])
        fallen_rocks += 1
        shape_index = next_circular_index(shape_index, 5)
        shape = shapes_[shape_index]
    return highest_point

def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/17.ex")
    jets = data[0]
    shapes = [Shape([(0,0), (1,0), (2,0), (3,0)], 1, 4),
              Shape([(1,0), (0,1), (1,1), (2,1), (1,2)], 3, 3),
              Shape([(2,0), (2,1), (0,2), (1,2), (2,2)], 3, 3),
              Shape([(0,0), (0,1), (0,2), (0,3)], 4, 1),
              Shape([(0,0), (1,0), (0,1), (1,1)], 2, 2)]

    highest_point = let_rocks_fall(shapes, jets, 2022)
    logging.info(f"The tower's height is {highest_point} units.")


    big_count = 1_000_000_000_000
    period = len(shapes)*len(jets)
    periodic_height = let_rocks_fall(shapes, jets, period)
    # do the periodic shape interleave? if so, by how much?
    interleaving_depth = 3
    # the division is probably not without rest, count the height of the rest
    total_height = periodic_height*(big_count//period) + let_rocks_fall(shapes, jets, big_count%period)
    total_height -= interleaving_depth*(big_count//period + (1 if big_count%period > 0 else 0))  # only gives a ROM
    print(total_height)
    # 1514285714288




start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9 :.3f} s")
