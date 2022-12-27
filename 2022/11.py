from functions import *

Monkey = typing.NewType("Monkey", None)


@dataclass()
class Monkey:
    items_: List[int]
    op_: str
    mod_: int
    destination_: Tuple[int, int]
    inspections_: int

    def take_turn(self, others_: Dict[int, Monkey], stress_reducer_: int, mod_all_: int) -> None:
        """ Computes a monkey turn and updates pther monkeys. """
        self.inspections_ += len(self.items_)
        while self.items_:
            item = self.items_.pop(0)
            item = eval(self.op_, {"old": item})
            item = item//stress_reducer_
            if item % self.mod_ == 0:
                dest_monkey = others_[self.destination_[0]]
            else:
                dest_monkey = others_[self.destination_[1]]
            if stress_reducer_ == 1:
                dest_monkey.items_.append(item % mod_all_)
            else:
                dest_monkey.items_.append(item)


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/11.in")
    monkeys = {}
    for line in data:
        if line == "":
            monkeys[monkey_id] = Monkey(items, op, mod, [dest1, dest2], 0)
        elif line.startswith("Monkey"):
            monkey_id = int(line[6:-1])
        elif line.startswith("Starting items"):
            items = [int(n) for n in line.split(": ")[1].split(", ")]
        elif line.startswith("Operation"):
            op = line.split("= ")[1]
        elif line.startswith("Test"):
            mod = int(line.split()[-1])
        elif line.startswith("If true"):
            dest1 = int(line.split()[-1])
        else:
            dest2 = int(line.split()[-1])
    monkeys[monkey_id] = Monkey(items, op, mod, [dest1, dest2], 0)
    start_monkeys = copy.deepcopy(monkeys)

    for i in range(20):
        for monkey in monkeys:
            monkeys[monkey].take_turn(monkeys, 3, 1)
    insp = sorted([m.inspections_ for m in monkeys.values()])
    logging.info(f"The level of monkey business is {insp[-2] * insp[-1]}.")

    mod_all = reduce(lambda x, y: x*y, [m.mod_ for m in monkeys.values()])
    for i in range(10000):
        for monkey in start_monkeys:
            start_monkeys[monkey].take_turn(start_monkeys, 1, mod_all)
    insp = sorted([m.inspections_ for m in start_monkeys.values()])
    logging.info(f"The level of monkey business is now {insp[-2] * insp[-1]}.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")