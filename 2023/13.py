from functions import *

flip = {".": "#", "#": "."}


def count_reflected_lines(lines_: List[str]) -> int:
    for index, line in enumerate(lines_):
        if index == 0: continue
        reflection_index = index
        for k in range(1, index+1):
            if index+k > len(lines_):
                break
            if lines_[index-k] != lines_[index+k-1]:
                reflection_index = -1
                break
        if reflection_index > 0:
            return reflection_index
    return 0


def print_pattern(pattern):
    vertical_mirror = count_reflected_lines(pattern[1])
    horizontal_mirror = count_reflected_lines(pattern[0])
    header = "   "
    for i in range(len(pattern[1])):
        header += str(i).ljust(3)
    print(header)
    for k, row in enumerate(pattern[0]):
        print(str(k).rjust(2), "  ".join(row[:]))
    print(f"{horizontal_mirror=}, {vertical_mirror=}")


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/13.ex")
    data.append("")  # need empty line at the end to finish parsing

    rows, cols, summary, patterns = [], [], 0, []
    for line in data:
        if line == "":
            # print_pattern(pattern)
            # input(f"Press ENTER to continue... {pattern_index + 1}/{len(patterns)}\n")
            summary += count_reflected_lines(cols) + 100*count_reflected_lines(rows)
            patterns.append((cols, rows))
            rows, cols = [], []
        else:
            rows.append(line)
            if not cols:
                cols = [""]*len(line)
            for i, c in enumerate(line):
                cols[i] += c
    logging.info(f"Part 1: {summary=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
