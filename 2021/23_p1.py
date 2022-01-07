from typing import *
from a_star import *

###### TYPES AND STUFF #######
cset = [".", "A", "B", "C", "D"]
# A State is a particular arrangement of the amphipods
State = Tuple[int]
# A Move defines, for a single amphipod, start->end and cost
Move = Tuple[int, float]
# (start, end): indexes to go through
Paths = Dict[Tuple[int,int], List[int]]


def get_moves(idx: int, conf: State, paths: Paths) -> List[Move]:
	""" Returns the list of possible moves, for a given amphipod,
		in a given configuration """
	#TODO: amphipod can actually move out of its room, can
	#		be useful for A to move a lot for instance
	moves = []
	cost_per_step = [0,1,10,100,1000][conf[idx]]
	# can only go in its own room, if empty or, if occupied by partner
	top_room_idx = conf[idx]+10
	low_room_idx = conf[idx]+14 # 11&15 for A, 12,16 for B, etc.
	# check if already at its destination
	if idx == low_room_idx:
		return []
	if (idx == low_room_idx and conf[top_room_idx]==conf[idx]):
		return []
	if (idx == top_room_idx and conf[low_room_idx]==conf[idx]):
		return []

	# room destinations
	if conf[top_room_idx] == 0 and conf[low_room_idx] == 0: # room is free, go at the bottom
		destinations = [low_room_idx]
	elif (conf[top_room_idx] not in [0,conf[idx]]) or (conf[low_room_idx] not in [0,conf[idx]]):
		destinations = [] # room is occupied by stranger
	else:
		destinations = [top_room_idx] # only case left

	# can go into the hallway, in authorized spots
	if idx >= 11:
		destinations += [0, 1, 3, 5, 7, 9, 10]

	# check for blocked paths
	for dest in destinations:
		path = paths[(idx, dest)][1:] # path includes starting position
		accessible = True
		for step in path:
			if conf[step] != 0:
				accessible = False
				break
		if accessible:
			cost = cost_per_step*len(path)
			moves.append( (dest, cost) )
	return moves

def allowed_states(	end: State, 
					state_space: Dict[State, 'Node'],
					paths: Paths,
					state: State) -> List['Node']:
	""" From a given state, returns the list of the possible
	(maybe not desirable) nodes, and  their associated cost. """
	nodes = []
	for i in [j for j in range(len(state)) if state[j] != 0 ]: # for amphipods
		for move in get_moves(i, state, paths):
			# Create new state, based on the move
			new_state = list(state)
			new_state[i] = 0 # leave the start position
			new_state[move[0]] = state[i] # get to the destination
			new_state = tuple(new_state)
			# Create new node based on the new state
			new_node = Node(new_state, move[1])
			if new_state == end:
				return [state_space[end]]
			# Add node to state space
			state_space[new_state] = new_node
			# Add node to list
			nodes.append( new_node )
	return nodes

def render(s: State) -> str:
	""" Creates a string representing the configuration """
	pic = f"#############\n#"
	for i in range(11):
		if i not in [2,4,6,8]:
			pic += cset[s[i]]
		else:
			pic += "-" # forbidden spot
	pic += f"#\n###{cset[s[11]]}#{cset[s[12]]}#{cset[s[13]]}#{cset[s[14]]}###\n"
	pic += f"  #{cset[s[15]]}#{cset[s[16]]}#{cset[s[17]]}#{cset[s[18]]}#\n"
	pic += "  #########"
	return pic

def distance(conf: State, paths: Paths, dest: List[int]) -> float:
	""" Returns the costs to move each amphipod to its target position,
		considering no blocking from others."""
	cost_per_step = lambda idx: [0,1,10,100,1000][conf[idx]]
	cost = 0
	for i in range(len(conf)):
		if conf[i] == 1 and i not in [11,15]: # A
			cost += cost_per_step(i)*(len(paths[(i, dest[0])])-1)
		if conf[i] == 2 and i not in [12,16]: # B
			cost += cost_per_step(i)*(len(paths[(i, dest[1])])-1)
		if conf[i] == 3 and i not in [13,17]: # C
			cost += cost_per_step(i)*(len(paths[(i, dest[2])])-1)
		if conf[i] == 4 and i not in [14,18]: # D
			cost += cost_per_step(i)*(len(paths[(i, dest[3])])-1)
	return cost

def find_path(start: int, end: int) -> List[int]:
	""" Find the shortest path between start and end """
	if start == end: return [start]
	neighbors = {	0: [1], 1:[0,2], 2:[1,11,3], 3:[2,4], 4:[3,12,5], 5:[4,6], 6:[5,13,7],
					7:[6,8], 8:[7,14,9], 9:[8,10], 10:[9], 11:[2,15], 12:[4,16], 13:[6,17],
					14:[8,18], 15:[11], 16:[12], 17:[13], 18:[14]}
	walked_paths = [[start]]
	valid_paths = []
	while walked_paths:
		new_walked_paths = []
		for path in walked_paths:
			could_move = False
			for n in neighbors[path[-1]]:
				if n == end:
					path.append(n)
					valid_paths.append(path)
					break
				elif n in path:
					continue
				else:
					new_path = path.copy()
					new_path.append(n)
					new_walked_paths.append( new_path )
		walked_paths = new_walked_paths
	best_path = list(range(100))
	for path in valid_paths:
		if len(path)<len(best_path):
			best_path = path
	return best_path

def list_paths() -> Paths:
	""" Lists all the indexes between a and b """
	paths = {}
	for start in range(19):
		for end in range(19):
			paths[(start, end)] = find_path(start, end)
	return paths

def main():
		########################
		#0 1 2 3 4 5 6 7 8 9 10# 
		#####11# 12# 13# 14#####
		    #15# 16# 17# 18#
		    ################

	# Paths: list of indexes to go through to go from a to b
	paths = list_paths()

	# Define start/end nodes
	#             0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18
	start_state = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 4, 2, 1, 4, 3) # input
	start_state = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 4, 1, 4, 3, 1)
	start_node = Node(start_state, 0.0)
	end_state = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 1, 2, 3, 4)
	end_node = Node(end_state, 0.0)
	state_space: Dict[State, 'Node'] = {}
	state_space[start_node.state] = start_node
	state_space[end_node.state] = end_node
	
	print(render(start_state))

	# Define A* functions
	heuristic = lambda s: distance(s, paths, [15, 16, 17, 18])
	get_next = lambda s: allowed_states(end_state, state_space, paths, s)

	# Get the optimal solution
	path = a_star(start_node, end_node, heuristic, get_next)
	print(render(path[0].state))
	for n in path: print(render(n.state))
	print(sum([n.cost for n in path])+distance(path[-2].state, paths, [11, 12, 13, 14]))

main()