from functions import *


def find_possible_records(record: str, counts: List[int]) -> List[str]:
    i = record.find("?")
    if i == -1:
        return [record]
    # check whether there is any chance this record could match the counts
    partial_count = count_record(record[:i])[:-1]
    if len(partial_count) > len(counts):
        return []
    if not all([counts[j] == partial_count[j] for j, _ in enumerate(partial_count)]):
        return []
    # continue with both the # and . options
    possible_records = []
    for r in find_possible_records(record[:i] + "#" + record[i+1:], counts):
        possible_records.append(r)
    for r in find_possible_records(record[:i] + "." + record[i+1:], counts):
        possible_records.append(r)
    return possible_records


def count_record(record: str) -> List[int]:
    return [len(c) for c in record.split(".") if "#" in c]


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/12.in")

    sum_counts = 0
    for line in data:
        record = line.split()[0]
        counts = list(map(int, line.split()[1].split(",")))
        all_records = find_possible_records(record, counts)
        matching_records = list(filter(lambda r: count_record(r) == counts, all_records))
        sum_counts += len(matching_records)
    logging.info(f"Part 1: {sum_counts=}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
