from typing import TypeVar
from functions import *

Cup = TypeVar("Cup")


@dataclass()
class Cup:
    ID_: int
    next_: Cup


class CupCircle:
    cup_ids_: Dict[int, Cup]

    def __init__(self, cups_: Cup):
        self.destination_ = None
        self.selected_ = cups_
        self.picked_up_ = None
        self.cup_ids_ = {}
        n = cups_.next_
        while n != cups_:
            self.cup_ids_[n.ID_] = n
            n = n.next_
        self.cup_ids_[n.ID_] = n
        self.highest_cup_ID_ = self.cup_ids_[max(self.cup_ids_.keys())].ID_

    def __repr__(self) -> str:
        rp = f"({self.selected_.ID_})"
        n = self.selected_.next_
        while n != self.selected_:
            rp += f" {n.ID_}"
            n = n.next_
        rp += "  ["
        rp += ", ".join([str(self.picked_up_.ID_), str(self.picked_up_.next_.ID_), str(self.picked_up_.next_.next_.ID_)])
        rp += f"]   => {self.destination_.ID_}"
        return rp

    def pick_up(self):
        """ Picks-up the next three cups after selected. """
        self.picked_up_ = self.selected_.next_
        self.selected_.next_ = self.picked_up_.next_.next_.next_
        self.picked_up_.next_.next_.next_ = None

    def find_destination(self):
        """ Finds the destination cup. """
        dest_id = self.selected_.ID_
        picked_ids = [self.picked_up_.ID_, self.picked_up_.next_.ID_, self.picked_up_.next_.next_.ID_]
        while True:
            dest_id -= 1
            if dest_id in picked_ids:
                continue
            if dest_id < 1:
                dest_id = self.highest_cup_ID_ + 1
            else:
                self.destination_ = self.cup_ids_[dest_id]
                break

    def insert_picked(self):
        """ Inserts cups after the destination cup. """
        after_dest = self.destination_.next_
        self.destination_.next_ = self.picked_up_
        self.picked_up_.next_.next_.next_ = after_dest

    def select_next(self):
        """ Selects the 'next' cup to play. """
        self.selected_ = self.selected_.next_

    def get_simple_rpr(self) -> str:
        """ Shows the 8 cups after the one numbered 1. """
        rp = ""
        start = self.cup_ids_[1]
        for i in range(8):
            start = start.next_
            rp += str(start.ID_)
        return rp

    def get_prod_after_1(self) -> int:
        """ Returns the product of the two cups after the cup ID 1. """
        prod = self.cup_ids_[1].next_.ID_
        prod *= self.cup_ids_[1].next_.next_.ID_
        return prod


def play_round(cups_: CupCircle, verbose_: bool = False):
    cups_.pick_up()
    cups_.find_destination()
    if verbose_: print(cups_)
    cups_.insert_picked()
    cups_.select_next()


def create_cups_from_input(in_: List[int]) -> Cup:
    first_cup = Cup(in_[0], None)
    prev = first_cup
    for c in in_[1:]:
        new_cup = Cup(c, None)
        prev.next_ = new_cup
        prev = new_cup
    prev.next_ = first_cup
    return first_cup


def main():
    logging.basicConfig(level=logging.INFO)
    data = [3, 8, 9, 1, 2, 5, 4, 6, 7]  # example
    data = [1, 2, 3, 4, 8, 7, 5, 9, 6]  # my input

    cups = CupCircle(create_cups_from_input(data))
    for i in range(100):
        play_round(cups, True)
    logging.info(f"The labels on cups after 1, after 100 moves is {cups.get_simple_rpr()}.")

    full_input = data+list(range(10, 1_000_001))
    first_cup = create_cups_from_input(full_input)
    cups = CupCircle(first_cup)
    for i in range(10_000_000):
        play_round(cups, False)

    logging.info(f"The product of labels of the two cups after 1, after 10 000 000 moves, is {cups.get_prod_after_1()}.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
