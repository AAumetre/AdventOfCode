from functions import *
import bisect

Position = Tuple[int, int, int]


def cube_to_faces(p_: Position) -> Set[Position]:
    # a cube is considered to measure 2x2 unit and, its position is given from the center
    return {(p_[0], p_[1]-1, p_[2]),
            (p_[0]+1, p_[1], p_[2]),
            (p_[0], p_[1]+1, p_[2]),
            (p_[0]-1, p_[1], p_[2]),
            (p_[0], p_[1], p_[2]-1),
            (p_[0], p_[1], p_[2]+1)}


def line_to_air_blocks(line_: List[int]) -> List[Tuple[Position, Position]]:
    """ Each tuple returned is the first and last air block of a continuous segment. First and last may be equal. """
    air_gaps = []
    if len(line_) == 1:
        return [] # no air if there's only one block
    air_start = line_[0]
    for i in range(len(line_)-1):
        if air_start + 2 == line_[i+1]: # move cursor right
            air_start = line_[i+1]
        else: # gap
            air_gaps.append((air_start+2, line_[i+1]-2))
            air_start = line_[i+1]
    return air_gaps


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/18.ex")
    # multiply cubes coordinates by 2, to keep int coordinates
    cubes = [tuple(map(lambda x: 2*int(x), line.split(","))) for line in data]

    faces = set()
    inside_faces = set()
    for cube in cubes:
        new_faces = cube_to_faces(cube)
        inside_faces = inside_faces.union(faces.intersection(new_faces))
        faces = faces.union(new_faces)
    unmerged_faces = faces.difference(inside_faces)
    print(f"The surface of the lava droplet is {len(unmerged_faces)} unit²")

    # build a dict with (x,y) as key and a list of z values, being each lava cube in the line
    # for each line of lava/air, compute the lists of consecutive air blocks
    # if a list of consecutive air blocks is bounded by the outside faces of the droplet, they should be ignored

    # option 1
    # we have a list of lists of consecutive trapped air blocks
    # trapped blocks can only be joined with blocks on x+1, x-1n y+1 and y-1
    # try merging as many lists of air blocks as possible
    # use part 1 to determine the surface area of all the air pockets

    # option 2
    # for each list: -2 unit²
    # repeat with (x,z) and (y,z) projections

    xy_proj, xz_proj, yz_proj = defaultdict(list), defaultdict(list), defaultdict(list)
    for block in cubes:
        bisect.insort(xy_proj[(block[0], block[1])], block[2])
        # bisect.insort(xz_proj[(block[0], block[2])], block[1])
        # bisect.insort(yz_proj[(block[1], block[2])], block[0])

    print(xy_proj)
    internal_air_gaps = []
    for xy, line in xy_proj.items():
        air_blocks = line_to_air_blocks(line)
        # eliminate air gaps which are part of the outside faces
        for air_gap in air_blocks:
            print(f"{xy=} {air_gap=}")
            first_faces = cube_to_faces((*xy, air_gap[0]))
            print(f"{first_faces=}")
            if unmerged_faces.intersection(first_faces) == first_faces:
                internal_air_gaps.append(air_gap)
            else:
                print(f"{unmerged_faces.intersection(first_faces)=}")
    print(f"{internal_air_gaps=}")




start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9 :.3f} s")
