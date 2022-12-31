from typing import List
from typing import Dict
from typing import Union
from typing import Callable
from typing import Tuple
from typing import Set
import typing
import collections
import builtins
import logging
import string
import logging
import functools
import itertools
import copy
import sys
import re
import math
from operator import mul
from collections import defaultdict
from functools import reduce
import time
from dataclasses import dataclass


def read_file(filename: str) -> List[str]:
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


def get_neighbor_indexes_manhattan(i: int, j: int, I: int, J: int) -> List[Tuple[int, int]]:
    """ Returns the list of the valid neighbors' indexes r=1, diagonals excluded"""
    neighbors = []
    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if i + 1 < I:
        neighbors.append((i + 1, j))
    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if j + 1 < J:
        neighbors.append((i, j + 1))
    return neighbors


def get_neighbor_indexes_euclidian(data: List, i: int, j: int) -> List[Tuple[int, int]]:
    """ Returns the list of neighbors, at Euclidian distance of 1 """
    indexes = []
    minusI = i - 1 >= 0
    minusJ = j - 1 >= 0
    plusI = i + 1 < len(data[0])
    plusJ = j + 1 < len(data)
    if minusJ and minusI: indexes.append((i - 1, j - 1))
    if minusJ: indexes.append((i, j - 1))
    if minusJ and plusI: indexes.append((i + 1, j - 1))
    if minusI: indexes.append((i - 1, j))
    if plusI: indexes.append((i + 1, j))
    if plusJ and minusI: indexes.append((i - 1, j + 1))
    if plusJ: indexes.append((i, j + 1))
    if plusJ and plusI: indexes.append((i + 1, j + 1))
    return indexes


def get_neighbor_indexes_euclidian3(point: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """ Returns the list of neighbors, at Euclidian distance of 1, in 3 dimensions. """
    indexes = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                indexes.append((point[0] + i, point[1] + j, point[2] + k))
    indexes.remove((point[0], point[1], point[2]))
    return indexes


def get_neighbor_indexes_euclidian4(point: Tuple[int, int, int, int]) -> List[Tuple[int, int, int, int]]:
    """ Returns the list of neighbors, at Euclidian distance of 1, in 4 dimensions. """
    indexes = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    indexes.append((point[0] + i, point[1] + j, point[2] + k, point[3] + l))
    indexes.remove((point[0], point[1], point[2], point[3]))
    return indexes
