from functions import *


def update_crt(cycle_: int, line_: str, x_: int, screen_: List[str]):
    line_ += ("#" if cycle_ % 40 in [x_ - 1, x_, x_ + 1] else ".")
    if len(line_) == 40:
        screen_.append(line_)
        line_ = ""
    return line_, screen_


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/10.in")
    cycle = 0
    state = {}
    x = 1
    crt_screen = []
    pixel_line = ""
    for line in data:
        if line == "noop":
            pixel_line, crt_screen = update_crt(cycle, pixel_line, x, crt_screen)
            cycle += 1
            state[cycle] = x
        else:
            pixel_line, crt_screen = update_crt(cycle, pixel_line, x, crt_screen)
            cycle += 1
            state[cycle] = x
            pixel_line, crt_screen = update_crt(cycle, pixel_line, x, crt_screen)
            cycle += 1
            state[cycle] = x
            x += int(line.split()[1])
    n_cycles = [20, 60, 100, 140, 180, 220]
    logging.info(f"The sum of the six signal strength is {sum([n*state[n] for n in n_cycles])}.")

    for line in crt_screen:
        print(line)


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
