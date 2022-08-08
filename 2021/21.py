from typing import List
from typing import Callable
from typing import Tuple
import functools
import itertools
import copy
import numpy as np


def read_file(filename: str) -> List:
    """ Returns a list of the lines in the file """
    try:
        with open(filename, 'r') as f:
            data = []
            for line in f:
                data.append(line.strip())
            return data
    except IOError:
        print(f"Error when opening the {filename} file.")
        exit(1)


def next_i(i: int) -> int:
    next_i = i + 1
    if next_i > 100:
        next_i = 1
    return next_i


def part1(p1_pos: int, p2_pos: int):
    p1_score = 0
    p2_score = 0
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
    print(f"Player 1: {p1_score}, Player 2: {p2_score}, Rolls: {rolls}. => {rolls*min([p1_score, p2_score])}")


def next_pos(pos: int, move: int) -> int:
    new_pos = pos + move
    if new_pos > 10:
        new_pos -= 10
    return new_pos

def main():
    p1_pos = 7 #input
    # p1_pos = 4
    p2_pos = 1 #input
    # p2_pos = 8

    part1(p1_pos, p2_pos)

    score_limit = 21
    possible_moves = {"3": 1, "4": 3, "5": 6, "6": 7, "7": 6, "8": 3, "9": 1}
    scoreboard = [0,0]
    #          p1_pos, p1_score, p1_turn, p2_pos, p2_score : universes count
    games_to_play = {(p1_pos, 0, True, p2_pos, 0): 1}
    # pre-compute the new position for each player
    move_table = {}
    for i in range(10):
        for move in possible_moves:
            move_table[(i+1, move)] = next_pos(i+1, int(move))

    while games_to_play:
        new_games = {}
        for (p1_pos, p1_score, p1_turn, p2_pos, p2_score), universes in games_to_play.items():
            if p1_turn:
                for move, count in possible_moves.items():
                    new_position = move_table[(p1_pos, move)]
                    new_score = p1_score + new_position
                    new_count = universes * count
                    if new_score >= score_limit:
                        scoreboard[0] += new_count
                    else:
                        key = (new_position, new_score, False, p2_pos, p2_score)
                        new_games[key] = new_games.get(key, 0) + new_count
            else:
                for move, count in possible_moves.items():
                    new_position = move_table[(p2_pos, move)]
                    new_score = p2_score + new_position
                    new_count = universes * count
                    if new_score >= score_limit:
                        scoreboard[1] += new_count
                    else:
                        key = (p1_pos, p1_score, True, new_position, new_score)
                        new_games[key] = new_games.get(key, 0) + new_count
        games_to_play = new_games
    print(f"The score is {scoreboard}, the winning score is {max(scoreboard)}")

main()