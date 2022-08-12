from functions import *

Space = Set[Tuple[int,int,int]]
	
def run_cycles(space: Set[Tuple], cycles: int, get_neighbors: Callable) -> Set[Tuple]:
	for cycle_i in range(cycles):
		next_space = copy.deepcopy(space)
		inactive_neighbors = set()
		# process active cubes
		for active_cube in space:
			neighbors = get_neighbors(active_cube)
			active_count = 0
			for n in neighbors:
				if n in space:
					active_count += 1
				else: # add inactive neighbors to set, to be processed later
					inactive_neighbors.add( n )
			# update state according to number of active neighbors
			will_be_active = (active_count == 2) ^ (active_count == 3)
			if not will_be_active:
				next_space.remove(active_cube)
		# process inactive neighbors
		for inactive_cube in inactive_neighbors:
			neighbors = get_neighbors(inactive_cube)
			active_count = 0
			for n in neighbors:
				if n in space:
					active_count += 1
			if active_count == 3:
				next_space.add(inactive_cube)
		space = next_space
	return space

def main():
	logging.basicConfig(level=logging.INFO)
	data = read_file("data/17.in")
    
	initial_space_3d = set()
	initial_space_4d = set()
	for j in range(len(data)):		
		for i in range(len(data[0])):
			if data[j][i]=="#":
				initial_space_3d.add((i,j,0))
				initial_space_4d.add((i,j,0,0))
				
	space = run_cycles(initial_space_3d, 6, get_neighbor_indexes_euclidian3)
	logging.info(f"Part 1: after 6 cycles, there are {len(space)} active cubes.")
	
	space = run_cycles(initial_space_4d, 6, get_neighbor_indexes_euclidian4)
	logging.info(f"Part 2: after 6 cycles, there are {len(space)} active cubes.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns()-start_time) / 10 ** 9} s")
