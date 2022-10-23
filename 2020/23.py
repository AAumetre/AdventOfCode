from typing import TypeVar
from functions import *

Cup = TypeVar("Cup")
@dataclass()
class Cup:
    """ A cup is either a single cup, or a range of consecutive cups. """
    ID_: int
    next_: Cup
    is_range_: bool


class CupCircle:

    def __init__(self, selected_idx_: int, cups_: List[int]):
        self.cups_ = cups_.copy()
        self.selected_idx_ = selected_idx_
        self.selected_ = self.cups_[self.selected_idx_]
        self.destination_ = 0

    def __repr__(self) -> str:
        rp = ""
        for i, c in enumerate(self.cups_):
            if i == self.selected_idx_:
                rp += f" ({c})"
            else:
                rp += f" {c}"
        rp += f"   => {self.destination_}"
        return rp

    def pop_next(self) -> int:
        """ Pops the first cup, clockwise of the selected one. """
        next_cup_i = 0
        if self.selected_idx_ + 1 < len(self.cups_):
            next_cup_i = self.selected_idx_ + 1
        next_cup = self.cups_[next_cup_i]
        self.cups_.remove(next_cup)
        return next_cup

    def find_destination(self):
        """ Finds the destination cup. """
        if self.selected_ == min(self.cups_):
            label = max(self.cups_)
        else:
            label = self.selected_ - 1
            while label not in self.cups_:
                label -= 1
        self.destination_ = label

    def insert_cups(self, cups_: List[int]):
        """ Inserts cups after the destination cup. """
        target_idx = self.cups_.index(self.destination_)
        first = self.cups_[:target_idx+1]
        third = self.cups_[target_idx+1:]
        self.cups_ = first + cups_ + third

    def select_next(self):
        self.selected_idx_ = self.cups_.index(self.selected_) + 1
        if self.selected_idx_ == len(self.cups_):
            self.selected_idx_ = 0
        self.selected_ = self.cups_[self.selected_idx_]

    def get_simple_rpr(self) -> str:
        rp = ""
        idx = self.cups_.index(1)
        while len(rp) < len(self.cups_)-1:
            if idx + 1 < len(self.cups_):
                idx += 1
            else:
                idx = 0
            rp += str(self.cups_[idx])
        return rp

    def get_product(self) -> int:
        idx = self.cups_.index(1)
        prod = 1
        to_find = 2
        while to_find > 0:
            if idx + 1 < len(self.cups_):
                idx += 1
                prod *= self.cups_[idx]
                to_find -= 1
            else:
                idx = 0
        return prod


def play_round(cups_: CupCircle) -> CupCircle:
    next_three = [cups_.pop_next() for i in range(3)]
    cups_.find_destination()
    cups_.insert_cups(next_three)
    cups_.select_next()
    print(cups_.cups_[:20], cups_.cups_[1000000-15:])
    return cups_


def main():
    logging.basicConfig(level=logging.INFO)
    input = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    # input = [1, 2, 3, 4, 8, 7, 5, 9, 6]
    cups = CupCircle(0, input)  # example
    cups = CupCircle(0, input)  # my input

   #for i in range(100):
    #    cups = play_round(cups)
    logging.info(f"The labels on cups after 1, after 100 moves is {cups.get_simple_rpr()}.")

    input = input + [i for i in range(10, 1000000-8)]
    cups = CupCircle(0, input)
    for i in range(4):
        cups = play_round(cups)
    logging.info(f"The product of labels of the two cups after 1, after 100000000 moves, is {cups.get_product()}.")
    # (3)8 9 1 2 5 4 6 7    10    999991   => 2
    #  3(2)8 9 1 5 4 6 7    10    999991   => 7
    #  3 2(5)4 6 7     10    999991 8 9 1  => 3
    #  3 4 6 7 2 5    (10)    999991 8 9 1   => 7
    #  3 4 6 7 2 5     10 (14)   999991 8 9 11 12 13 1  => 11 ...

    # 1->2   2->3   3->4   4->x    x->999    999->1



start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
