from functions import *

Position = Tuple[int, int]

@dataclass()
class Interval1D:  # forward declaration... because Python
    low_: int
    high_: int

class Interval1D:

    def __init__(self, a: int, b: int):
        self.low_ = a if a <= b else b
        self.high_ = b if self.low_ == a else a

    def __repr__(self) -> str:
        return f"[{self.low_},{self.high_}]"

    def is_unit(self) -> bool:
        return self.low_ == self.high_

    def is_inside(self, other_: Interval1D) -> bool:
        return self.low_ >= other_.low_ and self.high_ <= other_.high_

    def is_left_of(self, other_: Interval1D) -> bool:
        return self.high_ < other_.low_
    def is_right_of(self, other_: Interval1D) -> bool:
        return self.low_ > other_.high_

    def try_joining(self, other_: Interval1D) -> Tuple[bool, Interval1D]:
        if self.low_ <= other_.low_ <= self.high_ + 1:
            return True, Interval1D(self.low_, other_.high_)
        elif self.low_ - 1 <= other_.high_ <= self.high_:
            return True, Interval1D(other_.low_, self.high_)
        else:
            return False, Interval1D(0, 0)

class PiecewiseInterval1D:

    def __init__(self, initial_: Interval1D):
        self.pi_ = [initial_]

    def __repr__(self) -> str:
        rep = "{ "
        for interval in self.pi_:
            rep += interval.__repr__() + " "
        return rep + "}"

    def get_size(self) -> int:
        return len(self.pi_)

    def add_interval(self, new_: Interval1D) -> None:
        """ Add an interval to the list of intervals. """
        if not self.pi_:
            self.pi_ = [new_]
            return
        for current_index, interval in enumerate(self.pi_):
            joint_is_successful, joint_interval = interval.try_joining(new_)
            if new_.is_inside(interval):
                return # nothing to do, already covered
            elif interval.is_inside(new_):
                del self.pi_[current_index]
                return self.add_interval(new_)
            elif joint_is_successful:
                del self.pi_[current_index] # delete the element that was joined with the new interval
                return self.add_interval(joint_interval)
            elif new_.is_left_of(interval): # no join possible but left of current => insert left of current_index
                self.pi_ = self.pi_[:current_index] + [new_] + self.pi_[current_index:]
                return
            else: # move up until can join or insert left
                continue
        # if we get there, we could not either join or insert left, we can append (right)
        self.pi_.append(new_)
        return


@dataclass(frozen=True)
class ExclusionZone:
    i_: int
    j_: int
    r_: int

    def get_intersection_with_row(self, row_: int) -> Tuple[bool, Interval1D]:
        """ Computes the range of columns at the intersection between a row and the zone. """
        row_zone_distance = abs(self.j_ - row_)
        if row_zone_distance > self.r_:
            return False, Interval1D(0, 0)
        else:
            side_span = self.r_-row_zone_distance
            return True, Interval1D(self.i_-side_span, self.i_+side_span)


def analyze_row(zones_, row_: int) -> PiecewiseInterval1D:
    row_intervals = PiecewiseInterval1D(Interval1D(-1, -1))
    for zone in zones_:
        reaches_zone, interval = zone.get_intersection_with_row(row_)
        if reaches_zone:
            row_intervals.add_interval(interval)
    return row_intervals

def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/15.in")

    zones = set()
    beacons = set()
    for line in data:
        sensor, beacon = line.split(": ")
        get_i = lambda s: int(s.split(",")[0].split("=")[1])
        get_j = lambda s: int(s.split(",")[1].split("=")[1])
        si, sj, bi, bj = get_i(sensor), get_j(sensor), get_i(beacon), get_j(beacon)
        beacons.add((bi, bj))
        r = abs(bi - si) + abs(bj - sj)
        zones.add(ExclusionZone(si, sj, r))

    row_of_interest = 2_000_000
    interval = analyze_row(zones, row_of_interest)
    logging.info(f"There are {interval.pi_[0].high_ - interval.pi_[0].low_} positions that cannot contain a beacon on "
                 f"row {row_of_interest}.")

    max_row = 4_000_000
    # Note: could have "cheated" and looked only for radius + 1 points for each sensor...
    for row in range(max_row):
        row_intervals = analyze_row(zones, row)
        if row_intervals.get_size() > 1:
            tuning_freq = 4_000_000*(row_intervals.pi_[1].low_ - 1) + row
            logging.info(f"The tuning frequency is {tuning_freq} Hz.")
            break
    # around 70s to run, terrible


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
