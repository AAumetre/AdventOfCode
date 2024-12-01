import heapq

from functions import *


@dataclass()
class Path:
    steps_: List[Tuple[int, int]]
    heatloss_: int
    last_step_dir_: str
    steps_same_dir_: int
    distance_: int

    def __lt__(self, other):
        return (self.heatloss_ + self.distance_) < (other.heatloss_ + other.distance_)  # f = g + h

def find_best_path(heatmap, step_generator: Callable) -> Path:
    max_i, max_j = len(heatmap), len(heatmap[0])

    def dist(step_) -> int:
        return abs(max_i - step_[0]) + abs(max_j - step_[1])

    path_map = defaultdict(Path)
    directions = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}
    open_paths = [
        Path([(0, 0)], 0, "R", 0, dist((0, 0))),
        Path([(0, 0)], 0, "D", 0, dist((0, 0)))]
    best_path, best_worst_heatloss = None, math.inf
    while open_paths and best_path is None:
        path = heapq.heappop(open_paths)
        for direction in directions.keys():
            new_step = step_generator(path, direction, max_i, max_j)
            if new_step is None:
                continue
            # update the path with the new step
            new_path = copy.deepcopy(path)
            new_path.steps_.append(new_step)
            new_path.distance_ = dist(new_step)
            new_path.heatloss_ += heatmap[new_step[0]][new_step[1]]
            # stop exploring paths that have practically no chance of being the best one
            # if new_path.heatloss_ + 6*new_path.distance_ > best_worst_heatloss:
            #     continue
            if new_path.last_step_dir_ == direction:
                new_path.steps_same_dir_ += 1
            else:
                new_path.steps_same_dir_ = 0
            new_path.last_step_dir_ = direction
            # check if not arrived at destination
            if new_step == (max_i-1, max_j-1):
                best_path = new_path
                break
            # use path map to check if a better path exists
            path_id = (new_step, direction, new_path.steps_same_dir_)
            if path_id in path_map:
                if path_map[path_id] > new_path:  # there is another path, which is worse than new_path
                    # remove the other path and restore the heap queue
                    open_paths.remove(path_map[path_id])
                    heapq.heapify(open_paths)
                    # add and keep track of the new path
                    heapq.heappush(open_paths, new_path)
                    path_map[path_id] = new_path
                    best_worst_heatloss = min(best_worst_heatloss, new_path.heatloss_ + 9*new_path.distance_)
                else:
                    continue  # the other path is better, stop exploring this one
            else:
                path_map[path_id] = new_path
                heapq.heappush(open_paths, new_path)
                best_worst_heatloss = min(best_worst_heatloss, new_path.heatloss_ + 9*new_path.distance_)
    return best_path

def main():
    logging.basicConfig(level=logging.INFO)
    heatmap = [list(map(int, line)) for line in read_file("data/17.ex2")]
    max_i, max_j = len(heatmap), len(heatmap[0])

    def step_part_1(path: Path, direction: str, max_i: int, max_j: int) -> None|Tuple[int, int]:
        directions = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}
        new_step = (path.steps_[-1][0] + directions[direction][0], path.steps_[-1][1] + directions[direction][1])
        # if out of bounds or already seen, skip
        if not (0 <= new_step[0] < max_i and 0 <= new_step[1] < max_j) or new_step in path.steps_:
            return None
        # check for number of steps in the same direction
        if path.last_step_dir_ == direction and path.steps_same_dir_ == 2:
            return None
        return new_step

    best_path = find_best_path(heatmap, step_part_1)
    for i in range(max_i):
        line = ""
        for j in range(max_j):
            line += "#" if (i, j) in best_path.steps_ else "."
        print(line)
    logging.info(f"Part 1: {best_path.heatloss_}")

    def step_part_2(path: Path, direction: str, max_i: int, max_j: int) -> None|Tuple[int, int]:
        directions = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}
        if direction != path.last_step_dir_ and path.steps_same_dir_ < 4:
            return None
        else:
            new_step = (path.steps_[-1][0] + directions[direction][0], path.steps_[-1][1] + directions[direction][1])
        # if out of bounds or already seen, skip
        if not (0 <= new_step[0] < max_i and 0 <= new_step[1] < max_j) or new_step in path.steps_:
            return None
        # check for number of steps in the same direction
        if path.last_step_dir_ == direction and path.steps_same_dir_ == 9:
            return None
        return new_step

    best_path = find_best_path(heatmap, step_part_2)
    for i in range(max_i):
        line = ""
        for j in range(max_j):
            line += "#" if (i, j) in best_path.steps_ else "."
        print(line)
    logging.info(f"Part 2: {best_path.heatloss_}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
