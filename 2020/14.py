from functions import *

class Memory:
    def __init__(self):
        self.mem = defaultdict(int)
        self.sum = 0

    def write(self, address_: int, val_: int):
        if address_ in self.mem:
            self.sum -= self.mem[address_]
        self.mem[address_] = val_
        self.sum += val_

def part1(data: List[str]) -> int:
    memory = Memory()
    mask = 0
    not_inv_mask = 0
    for line in data:
        if line[:4] == "mask":
            mask_str = line.split(" = ")[1]
            mask = int(mask_str.replace("X", "0"), 2)
            not_inv_mask  = ~int(mask_str.replace("1", "X").replace("0", "1").replace("X", "0"), 2)
            logging.debug(f"mask is now {mask} and not mask is {not_inv_mask}.")
        else:
            address = int(line.split(" = ")[0][:-1].replace("mem[", ""))
            number = int(line.split(" = ")[1])
            memory.write(address, (number|mask)&not_inv_mask)
    return memory.sum

def is_one(num_: int, idx_: int) -> bool:
    return ((num_ >> idx_) & 1) == 1

def generate_masks(base_mask: int, indexes: List[int]) -> List[int]:
    """ Returns a list of masks to apply """
    mask_list = []
    indexes.sort()
    for i in range(pow(2, len(indexes))):
        current_mask = 0
        for idx, v in enumerate(indexes):
            if is_one(i, idx):
                current_mask += (1 << v)
        mask_list.append(base_mask|current_mask)
    return mask_list

def part2(data: List[str]) -> int:
    memory = Memory()
    base_mask = 0
    inv_float_mask = 0
    indexes = []
    for line in data:
        if line[:4] == "mask":
            mask_str = line.split(" = ")[1]
            base_mask = int(mask_str.replace("X", "0"), 2)
            indexes = [(len(mask_str)-i-1) for i in range(len(mask_str)) if mask_str[i] == "X"]
            inv_float_mask = ~int(mask_str.replace("X", "1"), 2)
        else:
            base_address = int(line.split(" = ")[0][:-1].replace("mem[", ""))
            value = int(line.split(" = ")[1])
            for mask in generate_masks(base_mask, indexes):
                address = (base_address&inv_float_mask)|mask
                memory.write(address, value)
    return memory.sum

def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/14.in")

    logging.info(f"Part 1: the sum is {part1(data)}.")
    logging.info(f"Part 2: the sum is {part2(data)}.")

main()