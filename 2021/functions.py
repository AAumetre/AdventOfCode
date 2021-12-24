from typing import List
from typing import Callable
from typing import Tuple
import functools
from numpy import array
from numpy.linalg import norm
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

def transform(f: Callable, data: List) -> List:
    """ Applies a lambda to each element of the input and returns a new list """
    return [f(e) for e in data]

def get_number_increases(data: List) -> int:
    it = iter(data[1:])
    return len( [d for d in data if next(it, 0) > d] ) 

def filter_and_remove(data: List, keyword: str) -> List:
    """ Filters the input data with a keyword, removes it and returns a new list """
    filtered = filter( lambda x: keyword in x, data )
    filtered = transform( lambda x: x.replace(keyword, ""), filtered )
    return filtered

def transpose(data: List[List]) -> List[List]:
    """ Returns the transposed of the input matrix """
    return [ [row[i] for row in data] for i in range(len(data[0])) ]

def list_bits_to_int(data: List) -> int:
    """ MSB at index 0 """
    val = 0
    length = len(data)
    for i in range(length):
        val = val + data[length-i-1]*(2**i)
    return val

def sum_matrix_col_all(mat: List[List]) -> List:
    return [sum(row) for row in mat]

def sum_matrix_col(mat: List[List], idx: int) -> int:
    return sum_matrix_col_all(mat)[idx]

def fuel_conso(target: int, pos: List[int]) -> int:
	fuel = 0
	for p in pos:
		n = abs(p-target)
		fuel += n*(n+1)/2
	return fuel
	
def remove_chars(data: str, to_remove: List[str]) -> str:
	if len(to_remove) == 0:
		return data
	else:
		return remove_chars(data.replace(to_remove[0],""), to_remove[1:])
		
def decode_7seg(data: str) -> int:
	table = {"abcefg":0, "cf":1, "acdeg":2, "acdfg":3, "bcdf":4, "abdfg":5, "abdefg":6, "acf":7, "abcdefg":8, "abcdfg":9}
	return table["".join(sorted(data))]	
		
def get_neigh(i: int, j: int, I: int, J: int) -> List[List[int]]:
	""" Returns the list of the valid neighbors' indexes r=1, diagonals excluded"""
	neighbors = []
	if i-1 >= 0:
		neighbors.append( [i-1, j] )
	if i+1 < I:
		neighbors.append( [i+1, j] )
	if j-1 >= 0:
		neighbors.append( [i, j-1] )
	if j+1 < J:
		neighbors.append( [i, j+1] )
	return neighbors

def get_triplet_idxs(size: int) -> List[List[int]]:
	triplet_idxs = []
	idx_p = [0,0,0]
	while idx_p[0] < size:
		idx_p[1] = idx_p[0] + 1
		while idx_p[1] < size:
			idx_p[2] = idx_p[1] + 1
			while idx_p[2] < size:
				triplet_idxs.append( idx_p.copy() )
				idx_p[2] += 1
			idx_p[1] += 1
		idx_p[0] += 1
	return triplet_idxs

def get_duet_idxs(size: int) -> List[List[int]]:
	duet_idxs = []
	idx_p = [0,0]
	while idx_p[0] < size:
		idx_p[1] = idx_p[0] + 1
		while idx_p[1] < size:
			duet_idxs.append( idx_p.copy() )
			idx_p[1] += 1
		idx_p[0] += 1
	return duet_idxs
