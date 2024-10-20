from functions import *


def h(str_: str) -> int:
    val = 0
    for c in str_:
        val = (17 * (val + ord(c))) % 256
    return val


class Instruction:

    def __init__(self, str_: str):
        if str_[-1] == "-":
            self.type_is_equal_ = False
            self.label_ = str_[:-1]
        else:
            self.type_is_equal_ = True
            split = str_.split("=")
            self.label_ = split[0]
            self.focal_ = int(split[1])
        self.boxid_ = h(self.label_)


def find_label_in_box(label_: str, box_: List) -> int:
    index = -1
    for i in range(len(box_)):
        if box_[i][0] == label_:
            index = i
            break
    return index

def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/15.in")

    sum_h = sum(map(h, data[0].split(",")))
    logging.info(f"Part 1: {sum_h}")

    boxes = [[] for _ in range(256)]
    for inst in map(Instruction, data[0].split(",")):
        if inst.type_is_equal_:
            index = find_label_in_box(inst.label_, boxes[inst.boxid_])
            if index != -1:
                boxes[inst.boxid_][index] = inst.label_, inst.focal_
            else:
                boxes[inst.boxid_].append((inst.label_, inst.focal_))
        else:
            index = find_label_in_box(inst.label_, boxes[inst.boxid_])
            if index != -1:
                del boxes[inst.boxid_][index]

    focusing_power = 0
    for i, box in enumerate(boxes):
        for l, lens in enumerate(box):
            focusing_power += (1+i)*(1+l)*lens[1]
    logging.info(f"Part 2: {focusing_power}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
