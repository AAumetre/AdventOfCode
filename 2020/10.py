from functions import *

def count_options(adapters: List) -> int:
    """ Given a list of adapters, returns the number of options
        to go from the beginning to the end. """
    end = adapters[-1]
    options = 0
    in_progress = [adapters[0]]
    while in_progress:
        option = in_progress.pop()
        if option+1 in adapters:
            if option + 1 == end:
                options += 1
            else:
                in_progress.append(option+1)
        if option+2 in adapters:
            if option + 2 == end:
                options += 1
            else:
                in_progress.append(option+2)
        if option+3 in adapters:
            if option + 3 == end:
                options += 1
            else:
                in_progress.append(option+3)
    return options

def main():
    logging.basicConfig(level=logging.DEBUG)
    data = [int(e) for e in read_file("data/10.in")]
    data = [0] + sorted(data) + [data[-1]+3]

    diff = [0, 0, 0]
    for i in range(1, len(data)):
        diff[abs(data[i-1]-data[i])-1] += 1
    logging.info(f"Part 1: product of the jolt differences is {diff[0]*diff[2]}.")

    # create isolated groups (3-apart from the rest)
    three_apart = [0]
    for i in range(1, len(data)):
        if abs(data[i-1]-data[i]) == 3:
            three_apart.append(i-1)
            three_apart.append(i)
    groups = [] # the groups are pairs of the list above
    for i in range(0, len(three_apart)-1, 2):
        if three_apart[i + 1] - three_apart[i] > 1 :
            groups.append([three_apart[i], three_apart[i+1]])

    options = 1
    for group in groups:
        # for each isolated group, compute the number of arrangements
        options *= count_options(data[group[0] : group[1]+1])
    logging.info(f"Part 2: number of options is {options}.")



main()