from functions import *

Tile = typing.NewType("Tile", None)
Position = Tuple[int, int]
TileId = Tuple[int, int]


@dataclass()
class Tile:
    up_: str
    left_: str
    down_: str
    right_: str
    matches_: List[List[TileId]]  # up, left, down, right

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
        self.matches_ = [[], [], [], []]

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

    def add_match(self, tile_id_: TileId, dir_: int) -> None:
        self.matches_[dir_].append(tile_id_)


# TODO: use this class in Tile as well
@dataclass()
class Image:
    pixels_: List[List[str]]

    def __init__(self, lines: List[str]):
        self.pixels_ = []
        for line in lines:
            self.pixels_.append(list(line))

    def transform(self, id_: int):  # {I, 1R, 2R, 3R, FH, FH1R, FH2R, FH3R}
        if id_ == 0:
            pass
        elif id_ == 1:
            self.rotate()
        elif id_ == 2:
            self.rotate()
            self.rotate()
        elif id_ == 3:
            self.rotate()
            self.rotate()
            self.rotate()
        elif id_ == 4:
            self.flip_hor()
        elif id_ == 5:
            self.flip_hor()
            self.rotate()
        elif id_ == 6:
            self.flip_hor()
            self.rotate()
            self.rotate()
        elif id_ == 7:
            self.flip_hor()
            self.rotate()
            self.rotate()
            self.rotate()

    def transpose(self, data_: List[List[str]]) -> List[List[str]]:
        return [[row[i] for row in data_] for i in range(len(data_[0]))]

    def rotate(self):
        cols = self.transpose(self.pixels_)
        self.create_from_lines(cols[::-1])

    def flip_hor(self):
        cols = self.transpose(self.pixels_)
        for i, col in enumerate(cols):
            cols[i] = col[::-1]
        self.create_from_cols(cols)

    def create_from_lines(self, lines_: List[List[str]]):
        for i, line in enumerate(lines_):
            self.pixels_[i] = line

    def create_from_cols(self, cols_: List[List[str]]):
        lines = self.transpose(cols_)
        for i, line in enumerate(lines):
            self.pixels_[i] = line

    def render(self) -> str:
        out_str = "\n"
        for line in self.pixels_:
            for pixel in line:
                out_str += pixel
            out_str += "\n"
        return out_str

    def count_pound_pattern(self, pattern_: List[List[int]]) -> int:
        count = 0
        height = len(pattern_)
        length = max([max(p) for p in pattern_])
        for j in range(len(self.pixels_) - height):
            for i in range(len(self.pixels_[0]) - length):
                match = True
                for line_offset, line in enumerate(pattern_):
                    for col_offset in line:
                        if self.pixels_[j + line_offset][i + col_offset] != "#":
                            match = False
                            break
                    if not match:
                        break
                if match:
                    count += 1
        return count

    def count_pounds(self) -> int:
        count = 0
        for line in self.pixels_:
            for pixel in line:
                if pixel == "#":
                    count += 1
        return count


@dataclass()
class ImageTile(Image):

    def __init__(self, lines: List[str]):
        cropped_lines = []
        for line in lines[1:-1]:
            cropped_lines.append(list(line[1:-1]))
        Image.__init__(self, cropped_lines)


class DirectionFinder:
    def __init__(self):
        # order is down, right, up, left
        # TODO: use numpy
        # self.directions_ = np.array([0,1],[1,0],[0,-1],[-1,0])
        self.directions_ = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.dir_index_ = 0

    def get_next(self):
        self.dir_index_ += 1
        self.dir_index_ %= len(self.directions_)
        return self.directions_[self.dir_index_]


def tile_factory(lines_: List[str]) -> List[Tile]:
    """ Returns a list of the possible tiles, in the following order:
		{I, 1R, 2R, 3R, FH, FH1R, FH2R, FH3R}. """
    tiles = []
    tile = Tile(lines_)  # I
    tiles.append(copy.deepcopy(tile))
    tile.rotate()  # 1R (one Pi/2 rotation)
    tiles.append(copy.deepcopy(tile))
    tile.rotate()  # 2R
    tiles.append(copy.deepcopy(tile))
    tile.rotate()  # 3R
    tiles.append(copy.deepcopy(tile))
    tile = Tile(lines_)
    tile.flip_hor()  # FH (flip horizontally)
    tiles.append(copy.deepcopy(tile))
    tile.rotate()  # FH1R (flip, then rotate)
    tiles.append(copy.deepcopy(tile))
    tile.rotate()  # FH2R
    tiles.append(copy.deepcopy(tile))
    tile.rotate()  # FH3R
    tiles.append(copy.deepcopy(tile))
    return tiles


def is_admissible(tiles_: Dict[TileId, Tile], puzzle_: Dict[Position, TileId], candidate_: Tile,
                  position_: Position) -> bool:
    """ Checks whether a given tile matches its neighbors - if any. """
    if (position_[0], position_[1] - 1) in puzzle_:  # look up
        if not puzzle_[(position_[0], position_[1] - 1)] in candidate_.matches_[0]:
            return False
    if (position_[0] - 1, position_[1]) in puzzle_:  # look left
        if not puzzle_[(position_[0] - 1, position_[1])] in candidate_.matches_[1]:
            return False
    if (position_[0], position_[1] + 1) in puzzle_:  # look down
        if not puzzle_[(position_[0], position_[1] + 1)] in candidate_.matches_[2]:
            return False
    if (position_[0] + 1, position_[1]) in puzzle_:  # look right
        if not puzzle_[(position_[0] + 1, position_[1])] in candidate_.matches_[3]:
            return False
    return True


def remove_from(open_: Dict[Position, Set[TileId]], tileId_: int) -> Dict[Position, Set[TileId]]:
    """ Remove a tile ID from all the possibilities in a dictionary and returns the result. """
    cleaned = open_.copy()
    for pos, pos_set in cleaned.items():
        cleaned[pos] = {p for p in pos_set if p[0] != tileId_}
    return cleaned


def compute_next_pos_dict(size_: int) -> Tuple[Dict[Position, Position], Position]:
    """ Compute the next position to explore, in a direct-rotating spiral.
		Also output the end position's coordinates. """
    # position = np.array([0,0])
    position = [0, 0]
    direction_finder = DirectionFinder()
    direction = direction_finder.directions_[0]
    res = {}
    done = False
    while not done:
        new_position = [position[0] + direction[0], position[1] + direction[1]]
        border_reached = new_position[0] == size_ or new_position[1] == size_ or new_position[0] < 0 or new_position[
            1] < 0
        if border_reached or tuple(new_position) in res:
            direction = direction_finder.get_next()
            new_position = [position[0] + direction[0], position[1] + direction[1]]
        res[(position[0], position[1])] = (new_position[0], new_position[1])
        position = new_position
        if len(res) == size_ * size_ - 1:
            done = True
    return res, tuple(new_position)


def solve_jigsaw(tiles_: Dict[TileId, Tile], open_: Dict[Position, Set[TileId]], puzzle_: Dict[Position, TileId],
                 next_pos_: Position, get_next_pos_: Dict[Position, Position], end_position_: Position) -> Tuple[
    Dict[Position, TileId], bool]:
    """ Solves a jigsaw puzzle. Should start at 0,0 ; will spiral down to the solution. """
    for possibility in open_[next_pos_]:
        if is_admissible(tiles_, puzzle_, tiles_[possibility], next_pos_):
            new_puzzle = puzzle_.copy()
            new_puzzle[next_pos_] = possibility
            if next_pos_ == end_position_:  # we're done
                return (new_puzzle, True)
            new_open = remove_from(open_, possibility[0])
            new_next_pos = get_next_pos_[next_pos_]
            (res, success) = solve_jigsaw(tiles_, new_open, new_puzzle, new_next_pos, get_next_pos_, end_position_)
            if success:
                return (res, success)
    return ({}, False)  # all the possibilities have been explored, no success


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/20.in")
    tiles = {}
    raw_image_tiles = {}
    i = 0
    # read the images and convert them to tiles
    while i < len(data):
        tile_id = int(data[i][5:-1])
        factory = tile_factory(data[i + 1:i + 11])
        for sub_id, tile in enumerate(factory):
            tiles[(tile_id, sub_id)] = tile
        raw_image_tiles[tile_id] = ImageTile(data[i + 1:i + 11])
        i += 12

    grid_s = int(math.sqrt(len(tiles) / 8))
    logging.info(f"The grid size is {grid_s}x{grid_s}.")

    # Find the corners, ie. tiles that only match others on 2 sides,
    # the sides, ie. the tiles that only match other on 3 sides,
    # and the rest.
    # Note: they are nice enough not to have put such tiles where the two
    #		sides are not up&down or left&right...
    corners = set()  # set of corner tile IDs, index
    unique_corners = set()  # for part 1
    sides = set()
    insides = set()
    for tile_id, tile in tiles.items():
        for other_tile_id, other_tile in tiles.items():
            if other_tile_id[0] == tile_id[0]:  # same tile, possibly different orientation
                continue
            if tile.match_up(other_tile):
                tile.add_match(other_tile_id, 0)
            if tile.match_left(other_tile):
                tile.add_match(other_tile_id, 1)
            if tile.match_down(other_tile):
                tile.add_match(other_tile_id, 2)
            if tile.match_right(other_tile):
                tile.add_match(other_tile_id, 3)
        n_matched_sides = sum([len(match_dir) > 0 for match_dir in tile.matches_])
        if n_matched_sides == 2:
            corners.add(tile_id)
            unique_corners.add(tile_id[0])
        elif n_matched_sides == 3:
            sides.add(tile_id)
        else:
            insides.add(tile_id)
    logging.info(f"The product of the corners' IDs is {reduce(mul, unique_corners)}.")

    # Recompose the puzzle
    # define an open jigsaw dictionary, which contains the possible tiles on each cell
    op_jigsaw = {}
    get_corner = lambda one, two: {c for c in corners if
                                   tiles[(c[0], c[1])].matches_[one] == [] and tiles[(c[0], c[1])].matches_[two] == []}
    op_jigsaw[(0, 0)] = get_corner(0, 1)  # top left corner
    op_jigsaw[(0, grid_s - 1)] = get_corner(1, 2)  # bottom left corner
    op_jigsaw[(grid_s - 1, 0)] = get_corner(3, 0)  # top right corner
    op_jigsaw[(grid_s - 1, grid_s - 1)] = get_corner(2, 3)  # bottom right corner
    # define the sides
    get_side = lambda one: {c for c in sides if tiles[(c[0], c[1])].matches_[one] == []}
    side_up = get_side(0)
    side_left = get_side(1)
    side_down = get_side(2)
    side_right = get_side(3)
    for j in range(1, grid_s - 1):
        op_jigsaw[(0, j)] = side_left
        op_jigsaw[(j, 0)] = side_up
        op_jigsaw[(j, grid_s - 1)] = side_down
        op_jigsaw[(grid_s - 1, j)] = side_right
    # and the inside tiles
    for j in range(1, grid_s - 1):
        for i in range(1, grid_s - 1):
            op_jigsaw[(i, j)] = insides

    # Join the tiles
    next_pos_dict, end_pos = compute_next_pos_dict(grid_s)
    solved_puzzle, _ = solve_jigsaw(tiles, op_jigsaw, {}, (0, 0), next_pos_dict, end_pos)
    # Compute the actual solved puzzle image
    image_pieces = {}
    for pos, tile_id in solved_puzzle.items():
        image = raw_image_tiles[tile_id[0]]
        image.transform(tile_id[1])
        image_pieces[pos] = image
    image_lines = []
    for j in range(grid_s):
        line = []
        for i in range(grid_s):
            line.append(image_pieces[(i, j)])
        image_lines.append(line)
    # regroup the parts of the images, line by line
    resulting_pixel_lines = []
    for image_line in image_lines:
        for line_idx in range(len(image_line[0].pixels_)):
            long_line = []
            for img in image_line:
                long_line += img.pixels_[line_idx]
            resulting_pixel_lines.append(long_line)
    big_picture = Image(resulting_pixel_lines)
    print(big_picture.render())

    # Look for monsters
    sea_monster = [[18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]
    for i in range(8):
        picture_copy = copy.deepcopy(big_picture)
        picture_copy.transform(i)
        monster_count = picture_copy.count_pound_pattern(sea_monster)
        if monster_count > 0:
            break
    not_part = big_picture.count_pounds() - monster_count * sum([len(l) for l in sea_monster])
    logging.info(f"There are {not_part} # which are not part of a sea monster.")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
