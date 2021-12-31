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

def next_i(i: int) -> int:
    next_i = i+1
    if next_i > 100:
        next_i = 1
    return next_i

def part1():
    i = 100
    p1_turn = True
    rolls = 0
    max_score = 1000
    while p1_score < max_score and p2_score < max_score:
        move = 0
        for r in range(3):
            i = next_i(i)
            move += i
        rolls += 3
        if p1_turn:
            p1_pos += move
            while p1_pos > 10:
                p1_pos -= 10
            p1_score += p1_pos
            p1_turn = False
        else:
            p2_pos += move
            while p2_pos > 10:
                p2_pos -= 10
            p2_score += p2_pos
            p1_turn = True
    print(f"Player 1: {p1_score}, Player 2: {p2_score}, Rolls: {rolls}.\n{rolls*min([p1_score, p2_score])}")

def next_pos(pos: int, move: int) -> int:
    new_pos = pos + move
    if new_pos > 10:
        new_pos -= 10
    return new_pos

def fill_rolls(history: dict, pos: int, score: int, rolls: List[int]) -> dict:
    for i in [1, 2, 3]:
        new_pos = next_pos(pos, i)
        new_score = score + new_pos
        new_rolls = rolls.copy()
        new_rolls.append( i )
        if new_score >= 21:
            key = ""
            for e in new_rolls:
                key += str(e)
            history[key] = len(new_rolls)
        else:
            history |= fill_rolls(history, new_pos, new_score, new_rolls)
    return history

def main():
    p1_score = 0
    # p1_pos = 7 #input
    p1_pos = 4
    p2_score = 0
    # p2_pos = 1 #input
    p2_pos = 8

    # part1()
    p1_rolls = {}
    print( fill_rolls(p1_rolls, p1_pos, 0, []) )
    p2_rolls = {}
    print("Player 2")
    print( fill_rolls(p2_rolls, p2_pos, 0, []) )
    
        
        

    
                

main()
