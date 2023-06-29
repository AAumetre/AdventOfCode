from functions import *


Part1Path = Tuple[str, frozenset, int]
Part2Path = Tuple[str, str, frozenset, int, str, str]

@dataclass()
class Valve:
    name_: str
    flow_rate_: int
    neighbors_: List


def compute_next_release(opened_valves_: frozenset, valves_: Dict[str, Valve], steps_: int = 1) -> int:
    release = 0
    for opened in opened_valves_:
        release += steps_*valves_[opened].flow_rate_
    return release


def clean_up(paths_: Set[Part1Path]) -> Set[Part1Path]:
    remaining_paths = defaultdict(int)
    for path in paths_:
        # if we're at the same place with the same valves opened, keep the one with the most released pressure
        remaining_paths[(path[0], path[1])] = max(remaining_paths[(path[0], path[1])], path[2])
    paths = set()
    for remaining_path in remaining_paths:
        paths.add((remaining_path[0], remaining_path[1], remaining_paths[remaining_path]))
    return paths

def clean_up_p2(paths_: Set[Part2Path]) -> Set[Part2Path]:
    remaining_paths = {}
    for path in paths_:
        # if we're at the same place with the same valves opened, keep the one with the most released pressure
        key = (path[0], path[1], path[2])
        new_max = path[3] if key not in remaining_paths else max(remaining_paths[key][0], path[3])
        remaining_paths[key] = (new_max, path[4], path[5])
    paths: Set[Part2Path] = set()
    for remaining_path in remaining_paths:
        paths.add((remaining_path[0], remaining_path[1], remaining_path[2], *remaining_paths[remaining_path]))
    return paths


def get_possible_paths(path_: Part1Path, valves_: Dict[str, Valve]) -> Set[Part1Path]:
    new_paths: Set[Part1Path] = set()
    next_pressure_released = path_[2] + compute_next_release(path_[1], valves_)
    # option 1: the local valve is closed, open it (if interesting)
    if path_[0] not in path_[1] and valves_[path_[0]].flow_rate_ > 0:
        new_opened = frozenset(list(path_[1]) + [path_[0]])
        new_paths.add((path_[0], new_opened, next_pressure_released + valves_[path_[0]].flow_rate_))
    # option 2: stay here and do nothing but let's not compute it
    # option 3: move
    for neighbor in valves_[path_[0]].neighbors_:
        new_paths.add((neighbor.name_, path_[1].copy(), next_pressure_released))
    return new_paths


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/16.ex")

    valves = {}
    for line in data:
        name = line.split(" has")[0][-2:]
        flow_rate = int(line.split(";")[0].split("=")[1])
        if "to valve " in line:
            others = [line.split("to valve ")[1]]
        else:
            others = line.split("to valves ")[1].split(", ")
        valves[name] = Valve(name, flow_rate, others)
        n_non_zero_valves = 0
    for valve in valves.values():
        # use references to valves, not strings
        valve.neighbors_ = list(map(lambda n: valves[n], valve.neighbors_))
        if valve.flow_rate_ > 0: n_non_zero_valves += 1

    timer = 1
    paths: Set[Part1Path] = {("AA", frozenset(), 0)}  # contains Tuple[position, set(opened valves), pressure released)
    while timer < 30:
        new_paths: Set[Part1Path] = set()
        for path in paths:
            next_pressure_released = path[2] + compute_next_release(path[1], valves)
            # option 1: the local valve is closed, open it (if interesting)
            if path[0] not in path[1] and valves[path[0]].flow_rate_ > 0:
                new_opened = frozenset(list(path[1]) + [path[0]])
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

    timer = 1
    # contains Tuple[list(positions), set(opened valves), pressure released)
    paths: Set[Part2Path] = {("AA","AA", frozenset(), 0, "AA", "AA")}
    while timer < 26:
        new_paths: Set[Part2Path] = set()
        for path in paths:
            idle_pressure_release = path[3] + compute_next_release(path[2], valves)
            # compute next possible path when you move (#3 is a change in pressure)
            new_paths_self = set()
            self_path = (path[0], path[2], path[3], path[4])
            if self_path[0] not in self_path[1] and valves[self_path[0]].flow_rate_ > 0:
                new_opened = frozenset(list(self_path[1]) + [self_path[0]])
                new_paths_self.add((self_path[0], new_opened, valves[self_path[0]].flow_rate_, ""))
            for neighbor in valves[self_path[0]].neighbors_:
                # if we're trying to get back to where we came from without having done anything... well, don't
                if neighbor.name_ != self_path[3]:
                    new_paths_self.add((neighbor.name_, self_path[1].copy(), 0, self_path[0]))
            # compute next possible path when the elephant moves (#3 is a change in pressure)
            new_paths_elef = set()
            elef_path = (path[1], path[2], path[3], path[5])
            if elef_path[0] not in elef_path[1] and valves[elef_path[0]].flow_rate_ > 0:
                new_opened = frozenset(list(elef_path[1]) + [elef_path[0]])
                new_paths_elef.add((elef_path[0], new_opened, valves[elef_path[0]].flow_rate_, ""))
            for neighbor in valves[elef_path[0]].neighbors_:
                if neighbor.name_ != elef_path[3]:
                    new_paths_elef.add((neighbor.name_, elef_path[1].copy(), 0, elef_path[0]))
            # iterate over the cross product of the two paths sets
            for cross in itertools.product(new_paths_self, new_paths_elef):
                if cross[0] == cross[1] and cross[0][1] != path[2]:  # we've opened the same valve twice
                    continue  # skip it, it's invalid
                resulting_path = (cross[0][0], cross[1][0], cross[0][1].union(cross[1][1]),
                                  cross[0][2]+cross[1][2]+idle_pressure_release,
                                  cross[0][3], cross[1][3])
                new_paths.add(resulting_path)
            # do the cross product between the paths or either you or the elephant
        # clean up the paths
        paths = clean_up_p2(new_paths)
        timer += 1
        logging.debug(f"{timer=}, paths: {len(paths)}")
        number_of_paths = len(paths)
        if number_of_paths > 1e5:
            paths_to_drop = sorted(paths, key=lambda x: x[3])[:int(number_of_paths/1.8)]
            for path in paths_to_drop:
                paths.remove(path)
            logging.debug(f"\tnew number of paths: {len(paths)}. Worst path: {paths_to_drop[0]}, best path: {paths_to_drop[-1]}")
    best_path = sorted(paths, key=lambda x: x[3])[-1]
    logging.debug(f"The best path is {best_path}.")
    logging.info(f"The maximum pressure that can be released is {best_path[3]} bar.")

start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9 :.3f} s")
