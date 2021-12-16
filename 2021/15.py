from typing import List
from typing import Callable
import heapq
		

class Node:
	def __init__(self, pos: List[int], blocking: bool, cost: float):
		self.pos = pos
		self.blocking = blocking
		self.cost = cost
		self.f = 0.0
		self.g = float("inf")
		self.h = 0.0
		self.parent = None
		self.closed = False
		self.in_opened = False


def a_star(world: List[List['Node']], start: List[int], end: List[int], heuristic: Callable, get_neighbours: Callable) -> List['Node'] :
	start_node = world[start[1]][start[0]]
	start_node.g = 0.0
	counter = 0 # used in case of tie on f and g
	opened_heap = []
	heapq.heappush(opened_heap, (0, 0, counter, start_node))
	path_found = False
	while not path_found:
		popped_element = heapq.heappop(opened_heap)
		current_node = popped_element[3]
		current_node.closed = True
		current_node.in_opened = False
		if current_node.pos == end:
			path_found = True
			break
		else:
			for n in get_neighbours(current_node.pos, world):
				if n.blocking or n.closed:
					continue
				new_g = current_node.g + n.cost
				if new_g < n.g or not n.in_opened:
					n.g = new_g
					n.h = heuristic(n.pos, end)
					n.f = n.g + n.h
					n.parent = current_node
					if not n.in_opened:
						counter += 1
						heapq.heappush(opened_heap, (n.f, n.g, counter, n))
						n.in_opened = True
	# build the path from start to end
	path = []
	node = world[end[1]][end[0]]
	while node.parent != None:
		path.append(node)
		node = node.parent
	return list(reversed(path))


def manhattan_neighbors(pos: List[int], world: List[List['Node']]) -> List[List[int]]:
	max = [len(world[0]), len(world)]
	neighbors_idx = []
	if pos[0]-1 >= 0:
		neighbors_idx.append([pos[0]-1, pos[1]])
	if pos[0]+1 < max[0]:
		neighbors_idx.append([pos[0]+1, pos[1]])
	if pos[1]-1 >= 0:
		neighbors_idx.append([pos[0], pos[1]-1])
	if pos[1]+1 < max[1]:
		neighbors_idx.append([pos[0], pos[1]+1])
	neighbors = []
	for idx in neighbors_idx:
		neighbors.append( world[idx[1]][idx[0]] )
	return neighbors


def manhattan_norm(pos: List[int], end: List[int]) -> int:
	return abs(end[0]-pos[0])+abs(end[1]-pos[1])

def main():
	data = [[int(e) for e in line.strip()] for line in open("15.in", "r")]
	cave_nodes = []
	for j in range(len(data)):
		cave_nodes.append([])
		for i in range(len(data[0])):
			cave_nodes[j].append( Node([i,j], False, data[j][i]) )

	path = a_star(cave_nodes, [0,0], [len(cave_nodes[0])-1, len(cave_nodes)-1], manhattan_norm, manhattan_neighbors)
	print( [e.cost for e in path] )
	print( sum([node.cost for node in path]) )

	large_cave_nodes = []
	scale = 5
	for j in range(scale*len(data)):
		large_cave_nodes.append([])
		for i in range(scale*len(data[0])):
			risk_ij = (data[j%len(data)][i%len(data[0])] + i//len(data[0]) + j//len(data))
			while risk_ij > 9: risk_ij -= 9
			large_cave_nodes[j].append( Node([i,j], False, risk_ij) )

	path = a_star(large_cave_nodes, [0,0], [len(large_cave_nodes[0])-1, len(large_cave_nodes)-1], manhattan_norm, manhattan_neighbors)
	print( [e.cost for e in path] )
	print( sum([node.cost for node in path]) )


main()
