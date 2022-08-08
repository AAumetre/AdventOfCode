from functions import *

def run(program: List) -> Tuple[int, int]:
    """ Runs the program until either the end is reached or,
        an infinite loop is detected.
        Returns the value of the accumulator. """
    executed = set({})
    i = 0
    accumulator = 0
    while i not in executed and i < len(program):
        executed.add(i)
        instruction = program[i]
        if instruction[0] == "acc":
            accumulator += instruction[1]
            i += 1
        elif instruction[0] == "jmp":
            i += instruction[1]
        else:
            i += 1
    return accumulator, i

def permute(program: List, index: int) -> List:
    """ Permutes jmp and nop and returns the resulting program. """
    mutated = program.copy()
    if program[index][0] == "nop":
        mutated[index] = ("jmp", program[index][1])
    elif program[index][0] == "jmp":
        mutated[index] = ("nop", program[index][1])
    else:
        logging.critical(f"Permute function received a wrong index: {program[index]} is not 'nop' or 'jmp'.")
        exit(1)
    return mutated

def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/08.in")

    program = []
    for line in data:
        program.append((line[:3], (1 if line[4] == "+" else -1)*(int(line[5:]))))

    acc, index = run(program)
    logging.info(f"Part 1: accumulator is {acc}.")

    permutation_index = 0
    while index != len(program):
        while program[permutation_index][0] not in ["nop", "jmp"]:
            permutation_index += 1
        mutated = permute(program, permutation_index)
        acc, index = run(mutated)
        permutation_index += 1

    logging.info(f"Part 2: accumulator is {acc}.")

main()