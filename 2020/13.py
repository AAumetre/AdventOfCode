import logging

from functions import *

def find_nearest(timestamp: int, busIds: List[int]) -> List[int]:
    best_bus = [0, timestamp]
    for id in busIds:
        possibilities = [math.floor(timestamp / id), math.ceil(timestamp / id)]
        for possibility in possibilities:
            time = possibility * id
            if time >= timestamp:
                if time - timestamp < best_bus[1]:
                    best_bus = [id, time - timestamp]
    return best_bus

def testBus(timestamp: int, busId: int) -> bool:
    """ Returns true is a given busId will show up at a given timestamp """
    return timestamp%busId == 0

def get_spread_from(spreads: Dict, pair: List[int]) -> int:
    if pair in spreads:
        return spreads[pair]
    else:
        return -spreads[pair[1], pair[0]]

def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/13.in")

    timestamp = int(data[0])
    busIds = [int(e) for e in data[1].split(",") if e != "x"]

    # part 1
    best_bus = find_nearest(timestamp, busIds)
    logging.info(f"Part 1: {best_bus[0]*best_bus[1]}")

    # part 2
    sortedBusIds = list(reversed(sorted(busIds)))
    logging.debug(f"Sorted bus IDs: {sortedBusIds}")
    # build map of spreads between IDs
    spreads = {}
    busesWithXs = data[1].split(",")
    for i in range(len(busesWithXs)):
        if busesWithXs[i] == "x":
            continue
        for j in range(i, len(busesWithXs)):
            if busesWithXs[j] == "x":
                continue
            spreads[(int(busesWithXs[i]), int(busesWithXs[j]))] = j-i
    get_spread = lambda x: get_spread_from(spreads, x)

    acc = 0
    sortedSpreads = []
    # compute the integral spread between the sorted bus IDs
    for pair in zip(sortedBusIds, sortedBusIds[1:]):
        acc += get_spread(pair)
        sortedSpreads.append(acc)
    logging.debug(f"Sorted spreads: {sortedSpreads}")

    nextTimestamp = reduce(mul, busIds)
    logging.debug(f"Starting timestamp: {nextTimestamp}")
    currentBus = 0
    delta = sortedBusIds[currentBus] # start with the highest period bus
    done = False
    while not done:
        nextTimestamp -= delta
        if testBus(nextTimestamp+sortedSpreads[currentBus], sortedBusIds[currentBus+1]):
            delta *= sortedBusIds[currentBus+1] # the period of the current pattern is getting greater
            currentBus += 1 # looking to match the next bus
            if currentBus == len(sortedBusIds) - 1: # we're done
                done = True
    # compute the spread between the first (highest) element, and the original first ID
    answer = nextTimestamp-get_spread((busIds[0], sortedBusIds[0]))
    logging.info(f"Part 2: {answer}")


main()