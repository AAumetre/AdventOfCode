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
    z7 = 26*z2 + w[6] + c[6]
    z9 = 26*z2 + w[8] + c[8]
    z11= 26*z2 + w[10] + c[10]
    w[4] = z4%26 + b[4]
    w[5] = z3%26 + b[5]
    w[7] = z7%26 + b[7]
    w[9] = z9%26 + b[9]
    w[11]= z11%26+ b[11]
    w[12]= z2%26 + b[12]
    w[13]= z1%26 + b[13]
    w_string = ""
    for e in w:
        if e > 9 or e <= 0:
            return "", False
        w_string += str(e)
    return w_string, True

def MONAD(model_number: str, A, B, C) -> Tuple[int,bool]:
    z = 0
    for i in range(len(A)):
        w = int(model_number[i])
        division = (z%26+B[i]==w)
        if A[i] == 26 and division:
            new_z = z // 26
        elif A[i] == 1 and not division:
            new_z = 26*z + w + C[i]
        else:
            return z, False
        #print(f"\tz_{i}=%12d\tw_{i}={w}\ta_{i}={A[i]}\tb_{i}={B[i]}\tc_{i}={C[i]} \t=> z_{i+1}={new_z}" %(z))                
        z = new_z
    return z, z==0

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
    
    w_seed = "1"*7
    cnt = 0
    finished = False
    valid = []
    while True:
        plausible = False
        while not plausible:
            w_seed = get_next(w_seed, 6)
            if w_seed == "9"*7:
                finished = True
                break
            model_number, plausible = get_plausible(w_seed, A, B ,C)
            cnt += 1
            if cnt%500000 == 0:
                print(f"Testing with seed: {w_seed}")
        if finished:
            break
        
        z, success = MONAD(model_number, A, B, C)
        if success:
            valid.append( int(model_number) )

    print(f"Max value: {max(valid)}")
    print(f"Min value: {min(valid)}")


main()
