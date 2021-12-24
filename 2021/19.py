from functions import *
from numpy import array

class Scanner():
	def __init__(self, name: str, points: List[List[int]]):
		self.name = name
		self.points = []
		for p in points:
			self.points.append( array(p) )
		self.offset = array([0,0,0])
			
	def translate(self, u: 'array') -> None:
		for p in range(len(self.points)):
			self.points[p] = self.points[p] + u
			
	def rotate(self, R: List['array']) -> None:
		for p in range(len(self.points)):
			tmp = R.dot(self.points[p])
			# tmp = self.points[p].dot(R)
			self.points[p] = tmp
			
	def match(self, other: 'Scanner') ->List['array']:
		matches = []
		for p0 in self.points:
			for p1 in other.points:
				if (p0 == p1).all():
					matches.append(p0)
		return matches
			
	def match12(self, other: 'Scanner') -> bool:
		limit = 11
		matches = 0
		compared = 0
		size = len(self.points)
		for p0 in self.points:
			compared += 1
			for p1 in other.points:
				if (p0 == p1).all():
					matches += 1
				if matches == limit:
					return True
				if (limit-matches) > (size-compared):
					return False

	
def transform_and_match(ref_sc: 'Scanner', other_sc: 'Scanner', rotations: List['array']) -> bool:
	for R in rotations:
		temp_sc = Scanner(f"tmp (copy of {other_sc.name})", other_sc.points)
		temp_sc.rotate(R)
		for p0_idx in range(len(ref_sc.points)):
			if (len(ref_sc.points) - p0_idx - 1) < 12:
				break 
			p0 = ref_sc.points[p0_idx]
			for p1 in temp_sc.points:
				u = array(p0-p1)
				temp_sc.translate( u )
				success = ref_sc.match12(temp_sc)
				if success:
					print(f"	Success matching 12 points of {other_sc.name} to {ref_sc.name}!")
					other_sc.rotate(R)
					other_sc.translate(u)
					other_sc.offset = u
					return True
				else:
					temp_sc.translate( -u )
	print(f"	Failed to find a transformation of {other_sc.name} to match at least 12 points of {ref_sc.name}")
	return False
		
def get_all_halfPi_rotations() -> List['array']:
	""" Returns a list of all the Pi/2 possible rotations """
	I = array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
	X = array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
	Y = array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
	r_list = [	[I],[X],[Y],[X,X],[X,Y],[Y,X],[Y,Y],[X,X,X],[X,X,Y],[X,Y,X],
				[X,Y,Y],[Y,X,X],[Y,Y,X],[Y,Y,Y],[X,X,X,Y],[X,X,Y,X],[X,X,Y,Y],
				[X,Y,X,X],[X,Y,Y,Y],[Y,X,X,X],[Y,Y,Y,X],[X,X,X,Y,X],[X,Y,X,X,X],
				[X,Y,Y,Y,X]]
	rotations = []
	for rot in r_list:
		total_rot = I
		for r in rot:
			total_rot = total_rot.dot(r)
		rotations.append(total_rot)
	return rotations			
		

def main():
	data = read_file("19.in")
	scanners = []
	i = 0
	while i<len(data):
		if "---" in data[i]:
			name = data[i].replace("--- ", "").replace(" ---","")
			points = []
			j = i+1
			while j<len(data) and data[j] != "":
				points.append([int(e) for e in data[j].split(",")])
				j += 1
			scanners.append( Scanner(name, points) )
			i = j+1
			
	
	rotations = get_all_halfPi_rotations()
	opened_scanners = scanners[1:]
	to_consider = []
	ref_sc = scanners[0]
	while len(opened_scanners) != 0:
		for s in opened_scanners:
			print(f"	opened_scanners {s.name}")
		found = False
		tmp_to_consider = []
		for other_sc in opened_scanners:
			print(f"Looking for {ref_sc.name}/{other_sc.name} intersection")
			found = transform_and_match(ref_sc, other_sc, rotations)
			if found:
				tmp_to_consider.append( other_sc )

		for tmp in tmp_to_consider:
			to_consider.append( tmp )
			opened_scanners.remove( tmp )
		if len(to_consider) == 0:
			print(f"FAILED to find any relations with {ref_sc.name}")
			exit(0)
		ref_sc = to_consider[0]
		for s in to_consider:
			print(f"	consider {s.name}")
		if len(to_consider)>1:
			to_consider = to_consider[1:]
		else:
			to_consider = []
			
	beacons = []
	for sc in scanners:
		for pt in sc.points:
			match =False
			for bc in beacons:
				if (pt == bc).all():
					match = True
					break
			if not match:
				beacons.append( pt )
	print(len(beacons))
	
	offsets = []
	for sc in scanners:
		offsets.append( sc.offset )
	distances = []
	k = 0
	for of1 in offsets:
		k += 1
		for of2 in offsets[k:]:
			distances.append(abs(of1[0]-of2[0])+abs(of1[1]-of2[1])+abs(of1[2]-of2[2]))
	print( max(distances) )


main()
