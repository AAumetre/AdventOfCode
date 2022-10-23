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
    def __init__(self, cups_: Cup):
        self.dest_ = None
        self.selected_ = cups_
        self.picked_up_ = [None]*3

    def __repr__(self) -> str:
        rp = f"({self.selected_.ID_})"
        n = self.selected_.next_
        while n != self.selected_:
            rp += f" {n.ID_}"
            n = n.next_
        rp += f"   => {self.dest_}"
        return rp

    def pick_up(self):
        """ Picks-up the next three cups after selected. """
        c = self.selected_
        for i in range(3):
            c = c.next_
            self.picked_up_[i] = c
        self.selected_.next_ = self.picked_up_[2].next_
        self.picked_up_[2].next_ = None # precaution

    def find_destination(self):
        """ Finds the destination cup. """
        dest_id = self.selected_.ID_ - 1
        found = False
        while not found:
            # check for lower-bound
            if dest_id < 1:
                # look for the highest cup ID
                highest = Cup(0, None, False)
                n = self.selected_.next_
                while n != self.selected_:
                    if n.ID_ > highest.ID_:
                        highest = n
                    n = n.next_
                self.dest_ = highest
                found = True
            else:
                # check if it was not picked up
                dest_is_picked_up = False
                for c in self.picked_up_:
                    if c.ID_ == dest_id:
                        dest_is_picked_up = True
                        break
                # look for dest_id in remaining cups, we know it's there
                if not dest_is_picked_up:
                    n = self.selected_.next_
                    while True:
                        if n.ID_ == dest_id:
                            self.dest_ = n
                            found = True
                            break
                        n = n.next_
            dest_id -= 1

    def insert_picked(self):
        """ Inserts cups after the destination cup. """
        after_dest = self.dest_.next_
        self.dest_.next_ = self.picked_up_[0]
        self.picked_up_[2].next_ = after_dest

    def select_next(self):
        """ Selects the 'next' cup to play. """
        self.selected_ = self.selected_.next_

    def get_simple_rpr(self) -> str:
        """ Shows the 8 cups after the one numbered 1. """
        rp = ""
        # find cup number 1
        start = self.selected_
        while start.ID_ != 1:
            start = start.next_
        for i in range(8):
            start = start.next_
            rp += str(start.ID_)
        return rp


def play_round(cups_: CupCircle) -> CupCircle:
    cups_.pick_up()
    cups_.find_destination()
    cups_.insert_picked()
    cups_.select_next()
    return cups_


def main():
    logging.basicConfig(level=logging.INFO)
    input = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    input = [1, 2, 3, 4, 8, 7, 5, 9, 6]
    # initialize cups
    first_cup = Cup(input[0], None, False)
    prev = first_cup
    for c in input[1:]:
        new_cup = Cup(c, None, False)
        prev.next_ = new_cup
        prev = new_cup
    prev.next_ = first_cup

    cups = CupCircle(first_cup)

    for i in range(100):
        cups = play_round(cups)
    logging.info(f"The labels on cups after 1, after 100 moves is {cups.get_simple_rpr()}.")
    return

    input = input + [i for i in range(10, 1000000-8)]
    cups = CupCircle(0, input)
    for i in range(4):
        cups = play_round(cups)
    logging.info(f"The product of labels of the two cups after 1, after 100000000 moves, is {cups.get_simple_rpr()}.")
    # (3)8 9 1 2 5 4 6 7    10    999991   => 2
    #  3(2)8 9 1 5 4 6 7    10    999991   => 7
    #  3 2(5)4 6 7     10    999991 8 9 1  => 3
    #  3 4 6 7 2 5    (10)    999991 8 9 1   => 7
    #  3 4 6 7 2 5     10 (14)   999991 8 9 11 12 13 1  => 11 ...

    # 1->2   2->3   3->4   4->x    x->999    999->1



start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
