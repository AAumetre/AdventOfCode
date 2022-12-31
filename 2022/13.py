from functions import *


@pass_by_val
def cmp_pairs(left_, right_) -> int:
    """ Return values are: -1 fail, 0 continue, 1 valid. """
    logging.debug(f"Compare {left_} and {right_}.")
    if isinstance(left_, int) and isinstance(right_, int):
        if left_ < right_: return 1
        if left_ == right_: return 0
        if left_ > right_: return -1
    if isinstance(left_, list) and isinstance(right_, list):
        while left_ and right_:
            status = cmp_pairs(left_.pop(0), right_.pop(0))
            if status != 0:
                return status
        if left_ and not right_: return -1
        if not left_ and right_: return 1
        return 0
    if isinstance(left_, int): return cmp_pairs([left_], right_)
    if isinstance(right_, int): return cmp_pairs(left_, [right_])


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/13.in")

    valid_pairs_indices = 0
    messages = []
    for i in range(0, len(data), 3):
        left = eval(data[i])
        right = eval(data[i+1])
        messages += [left, right]
        if cmp_pairs(left, right) == 1:
            logging.debug(f"\tpair ({1+i//3}) is valid")
            valid_pairs_indices += 1+i//3
        else:
            logging.debug(f"\tpair ({1+i//3}) is NOT valid")
    logging.info(f"The sum of the valid pair indices is {valid_pairs_indices}.")

    first, second = [[2]], [[6]]
    messages += [first, second]
    messages = sorted(messages, key=functools.cmp_to_key(cmp_pairs), reverse=True)
    logging.info(f"The decoder key for the distress signal is {(messages.index(first)+1)*(messages.index(second)+1)}.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")