from functions import *


def energy(cells_: List[List[str]], beam_: Tuple[int, int, str], max_i_: int, max_j_: int) -> int:
    energized_cells = defaultdict(set)
    slash_mirror = {"L": "D", "R": "U", "U": "R", "D": "L"}
    backslash_mirror = {"L": "U", "R": "D", "U": "L", "D": "R"}
    beams = [beam_]  # i, j, direction in [L, R, U, D]
    while beams:
        beam = beams.pop()
        if (beam[0], beam[1]) in energized_cells and beam[2] in energized_cells[(beam[0], beam[1])]:
            continue
        energized_cells[(beam[0], beam[1])].add(beam[2])
        next_pos = (beam[0] + (beam[2] == "D") - (beam[2] == "U"), beam[1] + (beam[2] == "R") - (beam[2] == "L"))
        if next_pos[0] < 0 or next_pos[0] > max_i_ or next_pos[1] < 0 or next_pos[1] > max_j_:
            continue
        next_char = cells_[next_pos[0]][next_pos[1]]
        if next_char == ".":
            beams.append((next_pos[0], next_pos[1], beam[2]))
        elif next_char == "-":
            if beam[2] in ["U", "D"]:  # beam is split
                beams.append((next_pos[0], next_pos[1], "L"))
                beams.append((next_pos[0], next_pos[1], "R"))
            else:
                beams.append((next_pos[0], next_pos[1], beam[2]))
        elif next_char == "|":
            if beam[2] in ["L", "R"]:  # beam is split
                beams.append((next_pos[0], next_pos[1], "U"))
                beams.append((next_pos[0], next_pos[1], "D"))
            else:
                beams.append((next_pos[0], next_pos[1], beam[2]))
        elif next_char == "/":
            beams.append((next_pos[0], next_pos[1], slash_mirror[beam[2]]))
        elif next_char == "\\":
            beams.append((next_pos[0], next_pos[1], backslash_mirror[beam[2]]))
    return len(energized_cells)-1


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/16.in")
    data = [list(line) for line in data]
    max_i, max_j = len(data) - 1, len(data[0]) - 1

    energize_cells = energy(data, (0, -1, "R"), max_i, max_j)
    logging.info(f"Part 1: {energize_cells}")

    max_energy = 0
    for j in range(max_j+1):
        max_energy = max(max_energy, energy(data, (-1, j, "D"), max_i, max_j))
        max_energy = max(max_energy, energy(data, (max_i+1, j, "U"), max_i, max_j))
    for i in range(max_i+1):
        max_energy = max(max_energy, energy(data, (i, -1, "R"), max_i, max_j))
        max_energy = max(max_energy, energy(data, (i, max_j+1, "L"), max_i, max_j))
    logging.info(f"Part 2: {max_energy}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
