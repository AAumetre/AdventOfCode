from functions import *


@dataclass()
class ClosedRule:
    allowed_: Set[str]  # allowed characters
    id_: int


@dataclass()
class OpenRule:
    left_: List[int]
    right_: List[int]
    id_: int

    def __init__(self, raw_: str, id_: int) -> None:
        self.id_ = id_
        if "|" not in raw_:
            self.left_ = [int(e) for e in raw_.split(" ")]
            self.right_ = []
        else:
            self.left_ = [int(e) for e in raw_.split(" | ")[0].split(" ")]
            self.right_ = [int(e) for e in raw_.split(" | ")[1].split(" ")]

    def compile_left(self, closed_rules: Dict[int, ClosedRule]) -> Set[str]:
        left_set = set()
        if self.left_ == []:
            return left_set
        if len(self.left_) == 1:
            left_set = closed_rules[self.left_[0]].allowed_
        else:  # size 2 only
            cross = list(itertools.product(
                closed_rules[self.left_[0]].allowed_,
                closed_rules[self.left_[1]].allowed_))
            for e in cross:
                left_set.add(e[0] + e[1])
        return left_set

    def compile_right(self, closed_rules: Dict[int, ClosedRule]) -> Set[str]:
        right_set = set()
        if self.right_ == []:
            return right_set
        if len(self.right_) == 1:
            right_set = closed_rules[self.right_[0]].allowed_
        else:  # size 2 only
            cross = list(itertools.product(
                closed_rules[self.right_[0]].allowed_,
                closed_rules[self.right_[1]].allowed_))
            for e in cross:
                right_set.add(e[0] + e[1])
        return right_set


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/19.in")
    # read the rules
    line_idx = 0
    open_rules = {}
    closed_rules = {}
    while data[line_idx] != "":
        split_line = data[line_idx].split(": ")
        if split_line[1] == "\"a\"":
            closed_rules[int(split_line[0])] = ClosedRule({"a"}, int(split_line[0]))
        elif split_line[1] == "\"b\"":
            closed_rules[int(split_line[0])] = ClosedRule({"b"}, int(split_line[0]))
        else:
            open_rules[int(split_line[0])] = OpenRule(split_line[1], int(split_line[0]))
        line_idx += 1
    # compile the rules
    while len(open_rules) > 0:
        # find rules that can be compiled
        to_compile = []
        for idx, rule in open_rules.items():
            # all of its left and right rules must be closed
            # tester le cas left = []!!!
            left_are_closed = (sum([(r in closed_rules) for r in rule.left_]) == len(rule.left_))
            right_are_closed = (sum([(r in closed_rules) for r in rule.right_]) == len(rule.right_))
            if left_are_closed and right_are_closed:
                to_compile.append(rule)
        # compile them
        compiled_rules = []
        for rule in to_compile:
            left_set = rule.compile_left(closed_rules)
            right_set = rule.compile_right(closed_rules)
            compiled_rules.append(ClosedRule(left_set.union(right_set), rule.id_))
        # remove them from open
        for rule in compiled_rules:
            open_rules.pop(rule.id_)
            closed_rules[rule.id_] = rule
    # read and check messages
    matches = sum([line in closed_rules[0].allowed_ for line in data[line_idx + 1:]])
    logging.info(f"Part 1: there are {matches} valid messages.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
