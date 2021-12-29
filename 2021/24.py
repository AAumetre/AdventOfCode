from typing import List
from typing import Callable
from typing import Tuple
import functools
import itertools
import copy

def read_file(filename: str) -> List:
    """ Returns a list of the lines in the file """
    try:
        with open(filename, 'r') as f:
            data = []
            for line in f:
                data.append( line.strip() )
            return data
    except IOError:
        print(f"Error when opening the {filename} file.")
        exit(1)

def replace_i(number: str, digit: str, index: int) -> str:
    return number[:index] + digit + number[index+1:]
    
def get_prev(number: str, index: int) -> str:
    n = int(number[index]) - 1
    if n == 0:
        number = replace_i(number, "9", index)
        return get_prev(number, index-1)
    else:
        return replace_i(number, str(n), index)
    
def get_next(number: str, index: int) -> str:
    n = int(number[index]) + 1
    if n == 10:
        number = replace_i(number, "1", index)
        return get_next(number, index-1)
    else:
        return replace_i(number, str(n), index)

def get_plausible(seed: str, a, b, c) -> Tuple[str,bool]:
    """ Based on a seed, returns the only candidate, based on the rule
        that z should only increase when a=1, and decrease otherwise.
        This function is hard-coded: it only works with my data. """
    w = [0]*14
    w[0] = int(seed[0])
    w[1] = int(seed[1])
    w[2] = int(seed[2])
    w[3] = int(seed[3])
    w[6] = int(seed[4])
    w[8] = int(seed[5])
    w[10]= int(seed[6])
    z1 = w[0]+c[0]
    z2 = 26*z1 + w[1] + c[1]
    z3 = 26*z2 + w[2] + c[2]
    z4 = 26*z3 + w[3] + c[3]
    z11= 26*z2 + w[10] + c[10]
    w[4] = z4%26 + b[4]
    w[5] = z3%26 + b[5]
    z7 = 26*z2 + w[5] + c[5]
    w[7] = z7%26 + b[7]
    w[9] = z3%26 + b[9]
    w[11]= z11%26+ b[11]
    w[12]= z2%26 + b[12]
    w[13]= z1%26 + b[13]
    w_string = ""
    for e in w:
        if e > 9 or e <= 0:
            return "", False
        w_string += str(e)
    return w_string, True
    
        
def f(w, z, a, b, c) -> int:
    if (z%26+b) == w:
        return z//a
    else:
        return 26*(z//a)+w+c

def main():
    data = read_file("24.in")
    instructions = [line.split(" ") for line in data]
    
    A = []
    B = []
    C = []
    for i in range(len(data)//18):
        A.append( int(instructions[18*i + 4][2]) )
        B.append( int(instructions[18*i + 5][2]) )
        C.append( int(instructions[18*i + 15][2]) )

    print(f"A = {A}")
    print(f"B = {B}")
    print(f"C = {C}")
    
    w_seed = "9"*7
    # w_seed = "7"*7
    # w_seed = "8191111"
    # 81914571491381 - too high
    cnt = 0
    while True:
        plausible = False
        while not plausible:
            w_seed = get_prev(w_seed, 6) # part 1
            # w_seed = get_next(w_seed, 6) # part 2
            model_number, plausible = get_plausible(w_seed, A, B ,C)
            cnt += 1
            if cnt%10000 == 0:
                print(f"Testing with seed: {w_seed}")

        z = 0
        increase_count = 0
        print(f"Testing with model number: {model_number}")
        for i in range(len(A)):
            w = int(model_number[i])
            new_z = f(w, z, A[i], B[i], C[i])
            print(f"\tz_{i}={z}\tw_{i}={w}\ta_{i}={A[i]}\tb_{i}={B[i]}\tc_{i}={C[i]} \t=> z_{i+1}={new_z}")                
            if new_z > z:
                increase_count += 1
                if increase_count > 7:
                    break
            z = new_z
        if z == 0:
            print(f"New model number found! {model_number}")
            break


main()
