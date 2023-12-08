from functions import *


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/08.in")

    directions = [0 if d == "L" else 1 for d in data[0]]
    nodes = {}
    for line in data[2:]:
        nodes[line.split(" = ")[0]] = line[:-1].split(" = (")[1].split(", ")
    pos, steps = "AAA", 0
    while pos != "ZZZ":
        pos = nodes[pos][directions[steps%len(directions)]]
        steps += 1
    logging.info(f"Part 1: {steps=}")

    current_nodes = set(filter(lambda x: x.endswith("A"), nodes.keys()))
    steps, lengths = 0, []
    while current_nodes:
        current_nodes = set(map(lambda x: nodes[x][directions[steps % len(directions)]], current_nodes))
        steps += 1
        nodes_to_remove = set(filter(lambda x: x.endswith("Z"), current_nodes))
        if nodes_to_remove:
            lengths.append(steps)
            current_nodes = current_nodes.difference(nodes_to_remove)
    steps = math.lcm(*lengths)
    logging.info(f"Part 2: {steps=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
