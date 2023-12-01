import math
import random
from functions import *

Position = Tuple[int, int, int]


@dataclass
class Vertex:
    a_: Position
    b_: Position

    def __eq__(self, other_) -> bool:
        """ Vertex matching is symmetrical. """
        exact_match = self.a_ == other_.a_ and self.b_ == other_.b_
        cross_match = self.a_ == other_.b_ and self.b_ == other_.a_
        return exact_match or cross_match

    def __hash__(self):
        """ Vertex hashing is symmetrical. """
        return hash(tuple(sorted([*self.a_, *self.b_])))


@dataclass
class Face:
    pos_: Position
    dirp_: bool  # direction, true is positive

    def __eq__(self, other_) -> bool:
        return self.pos_ == other_.pos_

    def __hash__(self):
        return hash(self.pos_)


class OrientedFace(Face):
    def __eq__(self, other_):
        return self.pos_ == other_.pos_ and (self.dirp_ == other_.dirp_)

    def __hash__(self):
        return hash((self.pos_, self.dirp_))

    def get_axis(self) -> str:
        if self.pos_[2] % 2 != 0:  # face is facing +z or -z
            return "+z" if self.dirp_ else "-z"
        elif self.pos_[0] % 2 != 0:  # face is facing +x or -x
            return "+x" if self.dirp_ else "-x"
        elif self.pos_[1] % 2 != 0:  # face is facing +y or -y
            return "+y" if self.dirp_ else "-y"

    def get_orthogonal_faces_plus_minus(self) -> List[Set[Self]]:
        """ First element of the return list are the 4 faces in the direction of the base face. """
        axis = self.get_axis()[1]
        if axis == "z":
            return [{  # 4 faces orthogonal, up
                    OrientedFace((self.pos_[0] + 1, self.pos_[1],       self.pos_[2] + 1), not self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] + 1,   self.pos_[2] + 1), not self.dirp_),
                    OrientedFace((self.pos_[0] - 1, self.pos_[1],       self.pos_[2] + 1), self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] - 1,   self.pos_[2] + 1), self.dirp_)},
                    {  # 4 faces, orthogonal, down
                    OrientedFace((self.pos_[0] + 1, self.pos_[1],       self.pos_[2] - 1), self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] + 1,   self.pos_[2] - 1), self.dirp_),
                    OrientedFace((self.pos_[0] - 1, self.pos_[1],       self.pos_[2] - 1), not self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] - 1,   self.pos_[2] - 1), not self.dirp_)}]
        elif axis == "x":
            return [{  # 4 faces orthogonal, right
                    OrientedFace((self.pos_[0] + 1, self.pos_[1] - 1,   self.pos_[2]), self.dirp_),
                    OrientedFace((self.pos_[0] + 1, self.pos_[1],       self.pos_[2] - 1), self.dirp_),
                    OrientedFace((self.pos_[0] + 1, self.pos_[1] + 1,   self.pos_[2]), not self.dirp_),
                    OrientedFace((self.pos_[0] + 1, self.pos_[1],       self.pos_[2] + 1), not self.dirp_)},
                    {  # 4 faces, orthogonal, left
                    OrientedFace((self.pos_[0] - 1, self.pos_[1] - 1,   self.pos_[2]), not self.dirp_),
                    OrientedFace((self.pos_[0] - 1, self.pos_[1],       self.pos_[2] - 1), not self.dirp_),
                    OrientedFace((self.pos_[0] - 1, self.pos_[1] + 1,   self.pos_[2]), self.dirp_),
                    OrientedFace((self.pos_[0] - 1, self.pos_[1],       self.pos_[2] + 1), self.dirp_)}]
        elif axis == "y":
            return [{  # 4 faces orthogonal, forward
                    OrientedFace((self.pos_[0] + 1, self.pos_[1] + 1, self.pos_[2]), not self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] + 1, self.pos_[2] - 1), self.dirp_),
                    OrientedFace((self.pos_[0] - 1, self.pos_[1] + 1, self.pos_[2]), self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] + 1, self.pos_[2] + 1), not self.dirp_)},
                    {  # 4 faces, orthogonal, back
                    OrientedFace((self.pos_[0] + 1, self.pos_[1] - 1, self.pos_[2]), self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] - 1, self.pos_[2] - 1), not self.dirp_),
                    OrientedFace((self.pos_[0] - 1, self.pos_[1] - 1, self.pos_[2]), not self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] - 1, self.pos_[2] + 1), self.dirp_)}]

    def get_neighbor_faces(self) -> Set[Self]:
        """ Get immediately surrounding faces. """
        axis = self.get_axis()[1]
        neighbor_faces = set([a for b in self.get_orthogonal_faces_plus_minus() for a in b])
        if axis == "z":
            neighbor_faces = neighbor_faces.union({  # 4 faces around self
                    OrientedFace((self.pos_[0] + 2, self.pos_[1],       self.pos_[2]), self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] + 2,   self.pos_[2]), self.dirp_),
                    OrientedFace((self.pos_[0] - 2, self.pos_[1],       self.pos_[2]), self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1] - 2,   self.pos_[2]), self.dirp_)})
        elif axis == "x":
            neighbor_faces = neighbor_faces.union({  # 4 faces around self
                    OrientedFace((self.pos_[0], self.pos_[1],       self.pos_[2] + 2),  self.dirp_),
                    OrientedFace((self.pos_[0], self.pos_[1] + 2,   self.pos_[2]),      self.dirp_),
                    OrientedFace((self.pos_[0], self.pos_[1],       self.pos_[2] - 2),  self.dirp_),
                    OrientedFace((self.pos_[0], self.pos_[1] - 2,   self.pos_[2]),      self.dirp_)})
        elif axis == "y":
            neighbor_faces = neighbor_faces.union({  # 4 faces around self
                    OrientedFace((self.pos_[0] + 2, self.pos_[1], self.pos_[2]),        self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1], self.pos_[2] + 2),    self.dirp_),
                    OrientedFace((self.pos_[0] - 2, self.pos_[1], self.pos_[2]),        self.dirp_),
                    OrientedFace((self.pos_[0],     self.pos_[1], self.pos_[2] - 2),    self.dirp_)})
        return neighbor_faces

    def get_blocking_blocked(self) -> Dict[Self, Self]:
        """ Get pairs of blocking and blocked faces, start with the list of those faces. """
        blocking_blocked_list = self.get_orthogonal_faces_plus_minus()
        if self.get_axis()[0] == "-":  # reverse the list
            blocking_blocked_list = [blocking_blocked_list[1], blocking_blocked_list[0]]
        # how do we make the pairs? by matching on coordinates, depending on the axis of self
        blocking_blocked = {}
        for blocking in blocking_blocked_list[0]:
            for blocked in blocking_blocked_list[1]:
                # match on any but the self axis
                if self.get_axis()[1] == "x" and blocking.pos_[1] == blocked.pos_[1] and blocking.dirp_ != blocked.dirp_:
                    blocking_blocked[blocking] = blocked
                if self.get_axis()[1] == "y" and blocking.pos_[2] == blocked.pos_[2] and blocking.dirp_ != blocked.dirp_:
                    blocking_blocked[blocking] = blocked
                if self.get_axis()[1] == "z" and blocking.pos_[0] == blocked.pos_[0] and blocking.dirp_ != blocked.dirp_:
                    blocking_blocked[blocking] = blocked
        return blocking_blocked

    def get_stitchable_faces(self, all_faces_: Set[Self]) -> Set[Self]:
        """ Get pairs of blocking-blocked faces, start with the list of those faces. """
        blocking_blocked = self.get_blocking_blocked()
        blocked_faces = set()
        for blocking, blocked in blocking_blocked.items():
            if blocking in all_faces_:
                blocked_faces.add(blocked)
        return self.get_neighbor_faces().intersection(all_faces_).difference(blocked_faces)


@dataclass
class Cube:
    """ A cube is considered to measure 2x2 unit and, its position is given from the center. """
    p_: Position

    def __eq__(self, other_) -> bool:
        return self.p_ == other_.p_

    def __hash__(self):
        return hash(self.p_)

    def get_faces(self) -> Set[Face]:
        """ Generate a set of faces from a cube. """
        return {Face((self.p_[0], self.p_[1] - 1, self.p_[2]), False),
                Face((self.p_[0] + 1, self.p_[1], self.p_[2]), True),
                Face((self.p_[0], self.p_[1] + 1, self.p_[2]), True),
                Face((self.p_[0] - 1, self.p_[1], self.p_[2]), False),
                Face((self.p_[0], self.p_[1], self.p_[2] - 1), False),
                Face((self.p_[0], self.p_[1], self.p_[2] + 1), True)}

    def get_vertices(self) -> Set[Vertex]:
        """ Generate a set of vertices from a cube. """
        # define points first
        a = (self.p_[0] - 1, self.p_[1] - 1, self.p_[2] + 1)
        b = (self.p_[0] + 1, self.p_[1] - 1, self.p_[2] + 1)
        c = (self.p_[0] + 1, self.p_[1] - 1, self.p_[2] - 1)
        d = (self.p_[0] - 1, self.p_[1] - 1, self.p_[2] - 1)
        e = (self.p_[0] - 1, self.p_[1] + 1, self.p_[2] + 1)
        f = (self.p_[0] + 1, self.p_[1] + 1, self.p_[2] + 1)
        g = (self.p_[0] + 1, self.p_[1] + 1, self.p_[2] - 1)
        h = (self.p_[0] - 1, self.p_[1] + 1, self.p_[2] - 1)
        return {Vertex(a,b), Vertex(b,c), Vertex(c,d), Vertex(d,a), Vertex(e,f), Vertex(f,g), Vertex(g,h), Vertex(h,e),
                Vertex(a,e), Vertex(b,f), Vertex(c,g), Vertex(d,h)}


def get_outside_face_from_cubes(cubes_: List[Cube]) -> OrientedFace:
    """ Find a face that is - for sure - on the outside of a set of cubes. """
    ref_line_x, ref_line_y = cubes_[0].p_[0], cubes_[0].p_[1]
    largest_z = -math.inf
    for cube in cubes_:
        if cube.p_[0] == ref_line_x and cube.p_[1] == ref_line_y:
            # list all cubes that have the same (x, y) as the first one and record the line
            largest_z = max(largest_z, cube.p_[2])
    # by construction, the surface that is exterior is the z+ one
    return OrientedFace((ref_line_x, ref_line_y, largest_z + 1), True)


def get_list_connex_cubes(cubes_: Set[Cube]) -> List[Set[Cube]]:
    """ From a large set of cubes, build a list of sets of connex cubes. All the cubes in one of the result list
     have at least one vertex in common. """
    # need to build sets of connex cubes, matching on vertices, not faces!
    connex_sets_cubes = []
    opened_cubes = cubes_.copy()
    while opened_cubes:
        starting_cube = opened_cubes.pop()
        connex_cubes = {starting_cube}
        common_vertices = starting_cube.get_vertices()
        found_one = True
        while found_one:
            found_one = False
            for other_cube in opened_cubes:
                other_vertices = other_cube.get_vertices()
                if common_vertices.intersection(other_vertices):
                    common_vertices = common_vertices.union(other_vertices)
                    connex_cubes.add(other_cube)
                    found_one = True
            opened_cubes = opened_cubes.difference(connex_cubes)
        connex_sets_cubes.append(connex_cubes)
    return connex_sets_cubes


def stitch_outside_faces(cubes_: Set[Cube]) -> Set[OrientedFace]:
    # find one outside face to start from
    starting_outside_face = get_outside_face_from_cubes(list(cubes_))
    free_faces = set([OrientedFace(f.pos_, f.dirp_) for f in join_cubes_to_faces(list(cubes_))])
    # now, stitch all outside faces together, so that we have the set of outside faces
    opened_faces = free_faces.difference(set([starting_outside_face]))
    faces_to_stitch = {starting_outside_face}
    outside_faces = set()
    while faces_to_stitch:
        face_to_stitch = faces_to_stitch.pop()
        outside_faces.add(face_to_stitch)
        candidates = face_to_stitch.get_stitchable_faces(free_faces)
        can_be_stitched = opened_faces.intersection(candidates)
        faces_to_stitch = faces_to_stitch.union(can_be_stitched)
        opened_faces = opened_faces.difference(can_be_stitched)
    return outside_faces


def join_cubes_to_faces(cubes_: List[Cube]) -> Set[Face]:
    """ Counts the set of free faces, once all cubes have been joined. """
    faces = set()
    junction_faces = set()
    for cube in cubes_:
        new_faces = cube.get_faces()
        junction_faces = junction_faces.union(faces.intersection(new_faces))
        faces = faces.union(new_faces)
    return faces.difference(junction_faces)


def solution_partial(data):
    cubes = {tuple(map(int, l.split(','))) for l in data}
    sides = lambda x, y, z: {(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)}
    seen = set()
    todo = [(-1, -1, -1)]
    while todo:
        here = todo.pop()
        todo += [s for s in (sides(*here) - cubes - seen) if all(-1 <= c <= 25 for c in s)]
        seen |= {here}
    return [s for c in cubes for s in sides(*c)], seen


def solution(data):
    sp, seen = solution_partial(data)
    return sum([(s in seen) for s in sp])


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/18.in")
    # not 2512, 2524 is too high
    # data = ["1,1,3", "2,1,3", "3,1,3", "1,2,3", "2,2,3", "3,2,3", "1,3,3",          "3,3,3",
    #         "1,1,2", "2,1,2", "3,1,2", "1,2,2",          "3,2,2", "1,3,2", "2,3,2", "3,3,2",
    #         "1,1,1", "2,1,1", "3,1,1", "1,2,1",          "3,2,1", "1,3,1", "2,3,1", "3,3,1",
    #         "1,1,0", "2,1,0", "3,1,0", "1,2,0", "2,2,0", "3,2,0", "1,3,0", "2,3,0", "3,3,0"]  # should be 78 and 68
    # data = ["0,0,1", "-1,0,0", "0,1,0", "0,-1,0", "1,0,0", "0,0,-1",  # cross centered around 0,0,0
    #         "10,0,1", "9,0,0", "10,1,0", "10,-1,0", "11,0,0", "10,0,-1"]  # other cross around 10,0,0 should be 72, 60
    # data = ["0,0,0", "1,1,0", "1,0,1", "1,-1,0", "1,0,-1", "2,1,0", "2,0,1", "2,-1,0", "2,0,-1", "3,0,0"]

    # pb_size = 40
    #
    # results_agree = True
    # tries = 0
    # while results_agree:
    #     # generate a problem
    #     problem = set()
    #     while len(problem) < pb_size:
    #         problem.add((random.randint(0,3), random.randint(0,3), random.randint(0,3)))
    #         # problem.add((random.randint(4,6), random.randint(0,3), random.randint(0,3)))
    #     test_data = [f"{p[0]},{p[1]},{p[2]}" for p in problem]
    #     # solve it
    #     cubes = [Cube(tuple(map(lambda x: 2 * int(x), line.split(",")))) for line in test_data]
    #     connex_cube_sets = get_list_connex_cubes(set(cubes))
    #     total_surface = sum(list(map(lambda x: len(stitch_outside_faces(x)), connex_cube_sets)))
    #     results_agree = total_surface == solution(test_data)
    #     tries += 1
    #     if tries%10 == 0: print(f"{tries=}\t{len(connex_cube_sets)=},\t{total_surface=}")
    # print(test_data)
    # return



    # multiply cubes coordinates by 2, to keep integral coordinates
    cubes = [Cube(tuple(map(lambda x: 2 * int(x), line.split(",")))) for line in data]

    free_faces = join_cubes_to_faces(cubes)
    print(f"The total surface of the lava droplet is {len(free_faces)} unit²")

    connex_cube_sets = get_list_connex_cubes(set(cubes))
    print(f"There are {len(connex_cube_sets)} groups of connex cubes.")
    # check tha this looks legit by building sets of faces and vertices, and making sure there was no cross intersection

    total_surface = sum(list(map(lambda x: len(stitch_outside_faces(x)), connex_cube_sets)))
    print(f"The exterior surface of the lava droplet is {total_surface} unit²")
    print(f"Real answer is {solution(data)}")
    _, seen_solution = solution_partial(data)
    solution_faces = {}

    # checked that, starting from any external face, the result is the same



start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9 :.3f} s")
