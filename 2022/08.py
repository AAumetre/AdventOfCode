from functions import *


@dataclass()
class TreeInfo:
	height_: int
	visible_: bool
	scenic_score_: int
	
	
def main():
	logging.basicConfig(level=logging.INFO)
	data = read_file("data/08.in")
	forest = {}
	for j in range(len(data)):
		for i in range(len(data[0])):
			visible = False
			if i==0 or j==0 or i==len(data[0])-1 or j==len(data)-1:
				visible = True
			forest[(i,j)] = TreeInfo(int(data[j][i]), visible, 1)
	
	directions = [[1,0],[0,-1],[-1,0],[0,1]]
	for j in range(1, len(data)-1):
		for i in range(1, len(data[0])-1):
			blocked_directions = 0
			for d in directions:
				look_x, look_y = i+d[0], j+d[1]
				score_multiplier = 1
				bumped_tree = False
				while look_x < len(data[0]) and look_x >= 0 and look_y < len(data) and look_y >= 0:
					if forest[(look_x, look_y)].height_ >= forest[(i,j)].height_:
						blocked_directions += 1
						score_multiplier = max(abs(i-look_x), abs(j-look_y))
						bumped_tree = True
						break
					look_x += d[0]
					look_y += d[1]
				if not bumped_tree:
					score_multiplier = max(abs(i-look_x+d[0]), abs(j-look_y+d[1]))
				logging.debug(f"Tree {(i,j)}'s scenic score multiplier in direction {d} is {score_multiplier}.")
				forest[(i, j)].scenic_score_ *= score_multiplier
			if blocked_directions < 4:
				forest[(i, j)].visible_ = True
	
	visible_trees = sum([tree.visible_ for tree in forest.values()])
	logging.info(f"There are {visible_trees} visible trees in the forest.")
	max_score = max([tree.scenic_score_ for tree in forest.values()])
	logging.info(f"The maximum scenic score is {max_score}.")
	
	
start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
