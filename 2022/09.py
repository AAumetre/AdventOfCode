from functions import *

Pos = List[int]


def move_knot(h_pos_: Pos, k_pos_: Pos) -> Pos:
	""" Move a knot, relative to the previous knot. """
	if h_pos_[0] == k_pos_[0]:
		k_pos_[1] += (h_pos_[1]-k_pos_[1])//2
	elif h_pos_[1] == k_pos_[1]:
		k_pos_[0] += (h_pos_[0]-k_pos_[0])//2
	else:  # diagonal
		k_pos_[0] += (1 if h_pos_[0] > k_pos_[0] else -1)
		k_pos_[1] += (1 if h_pos_[1] > k_pos_[1] else -1)
	return k_pos_


def move_head(heading_: str, steps_: int, h_pos_: Pos, knots_: List[Pos]) -> Set:
	""" Move the head and the attached knots. """
	tail_places = set()
	directions = {"R": [1,0], "U": [0,1], "L": [-1,0], "D": [0,-1]}
	for _ in range(steps_):
		h_pos_[0] += directions[heading_][0]
		h_pos_[1] += directions[heading_][1]
		for i, k_pos in enumerate(knots_):
			prev_knot = (knots_[i-1] if i >0 else h_pos_) 
			if max(abs(prev_knot[0]-k_pos[0]), abs(prev_knot[1]-k_pos[1])) > 1:
				k_pos = move_knot(prev_knot, k_pos)
		tail_places.add(tuple(knots_[-1]))
	return tail_places


def main():
	logging.basicConfig(level=logging.INFO)
	data = read_file("data/09.in")
	Hpos = [0, 0]
	knots = [[0,0]]
	tail_places = set()
	for direction, steps in [line.split() for line in data]:
		tail_places = tail_places.union( move_head(direction, int(steps), Hpos, knots) )
	logging.info(f"The tail of the rope visited {len(tail_places)} different places.")
	
	Hpos = [0, 0]
	knots = [[0,0] for i in range(9)]
	tail_places = set()
	for direction, steps in [line.split() for line in data]:
		tail_places = tail_places.union( move_head(direction, int(steps), Hpos, knots) )
	logging.info(f"The tail of the rope now visited {len(tail_places)} different places.")
	
	
start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
