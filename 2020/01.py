from functions import *

def main():
    logging.basicConfig(level=logging.INFO)
    numbers = [int(e) for e in read_file("data/01.in")]
    for pair in itertools.product(numbers, numbers):
        if sum(pair)==2020:
            print(pair[0]*pair[1])
            break
    for triplet in itertools.product(numbers, numbers, numbers):
        if sum(triplet) == 2020:
            print(triplet[0]*triplet[1]*triplet[2])
            break
main()