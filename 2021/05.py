from functions import *



def main(): # Hydrothermal vents
	data = read_file("05.in")
	# get x1,y1 and x2,y2
	pairs = [[[int(val) for val in pair.split(",")] for pair in line.replace("\n", "").split(" -> ")]	for line in data]
	# create list of x,y spanned
	spanned = []
	for line in pairs:
		start = array( line[0] )
		end	= array( line[1] )
		curr	= start.copy()
		u = (end-start)/norm(end-start, 2)
		# filter-out diagonals
		if not((abs(u[0])==1 or abs(u[0])==0) and (abs(u[1])==1 or abs(u[1])==0)):
			pass
		to_add = []
		while norm(curr-start, 2) < norm(end-start, 2):
			to_add.append( curr )
			curr = curr + u
		to_add.append( end )
		# filter non-ints and doubles
		to_add = [[int(round(xy)) for xy in pair] for pair in to_add]
		for i in range(len(to_add)):
			if i>0:
				if to_add[i][0] != to_add[i-1][0] or to_add[i][1] != to_add[i-1][1]:
					spanned.append( to_add[i] )
			else:
				spanned.append( to_add[0] )			
	# store in map{x: {y: n}} by incrementing n
	points = {}
	for p in spanned:
		x = str( int(p[0]) )
		y = str( int(p[1]) )
		if x in points:
			if y in points[x]:
				points[x][y] += 1
			else:
				points[x][y] = 1
		else:
			points[x] = {y: 1}
	# browse map to find where n>2
	overlaps = 0
	for x in points:
		for y in points[x]:
			if points[x][y] >= 2: 
				overlaps += 1
	print(f"There are {overlaps} overlaps")
	

main()
