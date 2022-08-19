from functions import *

Tile = typing.NewType("Tile", None)


@dataclass()
class Tile:
	up_: str
	left_: str
	down_: str
	right_: str
	
	def __init__(self, lines: List[str]):
		self.up_ = lines[0]
		self.down_ = lines[-1][::-1]
		right = ""
		left = ""
		for line in lines:
			right += line[-1]
			left += line[0]
		self.right_ = right
		self.left_ = left[::-1]
		
	def match_up(self, other_: Tile) -> bool:
		return self.up_ == other_.down_[::-1]
		
	def match_left(self, other_: Tile) -> bool:
		return self.left_ == other_.right_[::-1]
		
	def match_down(self, other_: Tile) -> bool:
		return self.down_ == other_.up_[::-1]
		
	def match_right(self, other_: Tile) -> bool:
		return self.right_ == other_.left_[::-1]
		
	def flip_hor(self):
		self.left_ = self.left_[::-1]
		self.right_ = self.right_[::-1]
		new_up = self.down_[::-1]
		self.down_ = self.up_[::-1]
		self.up_ = new_up
		
	def rotate(self):
		""" Trigo Pi/2 rotation """
		new_up = self.right_
		self.right_ = self.down_
		self.down_ = self.left_
		self.left_ = self.up_
		self.up_ = new_up


@dataclass()
class PickedTile:
	tiles_: List[Tile] # {I, 1R, 2R, 3R, FH, FH1R, FH2R, FH3R}
	picked_: int
	# OPTIMIZE: compute all possible sides, associated to each of the transformation
	
	def __init__(self, lines: List[str]):
		self.picked_ = 0
		self.tiles_ = []
		tile = Tile(lines) # I
		self.tiles_.append(copy.copy(tile))
		tile.rotate() # 1R (one Pi/2 rotation)
		self.tiles_.append(copy.copy(tile))
		tile.rotate() # 2R
		self.tiles_.append(copy.copy(tile))
		tile.rotate() # 3R
		self.tiles_.append(copy.copy(tile))
		tile = Tile(lines)
		tile.flip_hor() # FH (flip horizontally)
		self.tiles_.append(copy.copy(tile))
		tile.rotate() # FH1R (flip, then rotate)
		self.tiles_.append(copy.copy(tile))
		tile.rotate() # FH2R
		self.tiles_.append(copy.copy(tile))
		tile.rotate() # FH3R
		self.tiles_.append(copy.copy(tile))
		
	def get_picked(self) -> Tile:
		return self.tiles_[picked_]
		
	def match(self, other_: Tile) -> List[int]:
		matched = []
		for index, tile in enumerate(self.tiles_):
			if sum(tile.match(other_)) > 0:
				matched.append(index)
		return matched
	
@dataclass()
class ImageTile:
	lines_: List[str]
	
	def __init__(self, lines: List[str]):
		self.lines_ = []
		for line in lines[1:-1]:
			self.lines_.append(line[1:-1])


def main():
	logging.basicConfig(level=logging.INFO)
	data = read_file("data/20.ex")
	tiles = {}
	image_tiles = {}
	i = 0
	while i < len(data):
		tile_id = int(data[i][5:-1])
		tiles[tile_id] = PickedTile(data[i+1:i+11])
		image_tiles[tile_id] = ImageTile(data[i+1:i+11])
		i += 12

	grid_s = int(math.sqrt(len(tiles)))
	logging.info(f"The grid size is {grid_s}x{grid_s}.")
	
	# Find the corners, ie. tiles that only match others on 2 sides
	# Note: they are nice enough not to have put such tiles where the two
	#		sides are not up&down or left&right...
	corners = set() # set of corner tile IDs, index and side matches
	for tile_id, tile in tiles.items():
		for index, t_tile in enumerate(tile.tiles_):
			t_matches = [0, 0, 0, 0] # up, left, down, right
			for other_tile_id, other_tile in tiles.items():
				if other_tile_id == tile_id:
					continue
				for other_t_tile in other_tile.tiles_:
					if t_tile.match_up(other_t_tile):
						t_matches[0] += 1
					if t_tile.match_left(other_t_tile):
						t_matches[1] += 1
					if t_tile.match_down(other_t_tile):
						t_matches[2] += 1
					if t_tile.match_right(other_t_tile):
						t_matches[3] += 1
					if sum(t_matches) > 2:
						break
			if sum(t_matches) == 2:
				print(tile_id, index, t_matches)
				corners.add((tile_id, index, tuple(t_matches)))
			if sum(t_matches) > 2:
				break
	unique_corners = set()
	for e in corners:
		unique_corners.add(e[0])
	logging.info(f"The product of the corners' IDs is {reduce(mul, unique_corners)}.")
	
	#for c in corners:
#		print(c)
			
	# Recompose the puzzle
	
	
	# Remove boundaries to create the image
	
	# Look for monsters
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	



start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns()-start_time) / 10 ** 9} s")
