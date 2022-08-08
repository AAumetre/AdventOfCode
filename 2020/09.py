from functions import *

def main():
    logging.basicConfig(level=logging.DEBUG)
    data = [int(e) for e in read_file("data/09.in")]

    window_size = 25
    index = window_size
    done = False
    while index < len(data) and not done:
        found_pair = False
        for i in range(index-window_size, index+window_size):
            for j in range(i, index+window_size):
                if data[i] == data[j]:
                    continue
                if (data[i] + data[j]) == data[index]:
                    found_pair = True
                    break
            if found_pair:
                break
        if not found_pair:
            done = True
        else:
            index += 1
    weak_number = data[index]
    logging.info(f"Part 1: first number that does not have said property {weak_number}.")

    for i in range(len(data)):
        acc = 0
        last_index = i
        while acc < weak_number:
            acc += data[last_index]
            last_index += 1
        if acc == weak_number:
            logging.info(f"Part 2: the encryption weakness is {min(data[i:last_index])+max(data[i:last_index])}.")
            break






main()