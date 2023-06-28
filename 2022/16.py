from functions import *

@dataclass()
class Valve:
    name_: str
    flow_rate_: int
    neighbors_: List


def compute_next_release(opened_valves_: frozenset, valves_: Dict[str, Valve]) -> int:
    release = 0
    for opened in opened_valves_:
        release += valves_[opened].flow_rate_
    return release


def clean_up(paths_: Set[Tuple[str, frozenset, int]]) -> Set[Tuple[str, frozenset, int]]:
    remaining_paths = defaultdict(int)
    for path in paths_:
        # if we're at the same place with the same valves opened, keep the one with the most released pressure
        remaining_paths[(path[0], path[1])] = max(remaining_paths[(path[0], path[1])], path[2])
    paths = set()
    for remaining_path in remaining_paths:
        paths.add((remaining_path[0], remaining_path[1], remaining_paths[remaining_path]))
    return paths


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/16.in")

    valves = {}
    for line in data:
        name = line.split(" has")[0][-2:]
        flow_rate = int(line.split(";")[0].split("=")[1])
        if "to valve " in line:
            others = [line.split("to valve ")[1]]
        else:
            others = line.split("to valves ")[1].split(", ")
        valves[name] = Valve(name, flow_rate, others)
    for valve in valves.values():
        valve.neighbors_ = list(map(lambda n: valves[n], valve.neighbors_))

    timer = 1
    paths: Set[Tuple[str, frozenset, int]] = {("AA", frozenset(), 0)}  # contains Tuple[position, set(opened valves), pressure released)
    while timer < 30:
        new_paths: Set[Tuple[str, frozenset, int]] = set()
        for path in paths:
            next_pressure_released = path[2] + compute_next_release(path[1], valves)
            # option 1: the local valve is closed, open it (if interesting)
            if path[0] not in path[1] and valves[path[0]].flow_rate_ > 0:
                new_opened = frozenset(list(path[1])+[path[0]])
                new_paths.add((path[0], new_opened, next_pressure_released + valves[path[0]].flow_rate_))
            # option 2: stay here and do nothing but let's not compute it
            # option 3: move
            for neighbor in valves[path[0]].neighbors_:
                new_paths.add((neighbor.name_, path[1].copy(), next_pressure_released))
        # clean up the paths
        paths = clean_up(new_paths)
        timer += 1
    best_path = sorted(paths, key=lambda x: x[2])[-1]
    logging.debug(f"The best path is {best_path}.")
    logging.info(f"The maximum pressure that can be released is {best_path[2]} bar.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
