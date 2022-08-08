from typing import List
from typing import Callable
import heapq

class Node:
	def __init__(self, state, cost: float):
		self.state = state
		self.cost = cost
		self.f = 0.0
		self.g = float("inf")
		self.h = 0.0
		self.parent = None
		self.closed = False
		self.in_opened = False

""" Implements the A* pathfinding algorithm, hopefully in a generic-enough way
	to be re-used.
	The 'state' in the Node used shall allow comparison with '=='.
	Advice: to implement the two functions (heuristic and get_next), you should
		use a lambda to bind arguments to a more general function. In particular,
		this allows to consider all the existing nodes, without the 'a_star' function
		needing them.
	The returned value is the list of nodes, from start to end."""
def a_star(	start: 'Node',
			end: 'Node',
			heuristic: Callable,	# Called on the Node's state, returns a float
			get_next: Callable		# Called on a Node's state, returns the list of nodes to explore
			) -> List['Node'] :
	start.g = 0.0
	counter = 0 # used in case of tie on f and g
	opened_heap = []
	heapq.heappush(opened_heap, (0, 0, counter, start))
	path_found = False
	while not path_found:
		popped_element = heapq.heappop(opened_heap)
		current_node = popped_element[3]
		current_node.closed = True
		current_node.in_opened = False
		if current_node.state == end.state:
			path_found = True
			break
		else:
			for n in get_next(current_node.state):
				if n.closed:
					continue
				new_g = current_node.g + n.cost
				if new_g < n.g or not n.in_opened:
					n.g = new_g
					n.h = heuristic(n.state)
					n.f = n.g + n.h
					n.parent = current_node
					if not n.in_opened:
						counter += 1
						heapq.heappush(opened_heap, (n.f, n.g, counter, n))
						n.in_opened = True
	# build the path from start to end
	path = []
	node = end
	while node.parent != None:
		path.append(node)
		node = node.parent
	return list(reversed(path))