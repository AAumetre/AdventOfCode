from functions import *

def main():
	data = read_file("13.in")
	
	middle = data.index("")
	points = [ [int(e.split(",")[0]), int(e.split(",")[1])] for e in data[:middle] ]
	syms = data[middle+1:]
	
	decode_sym = lambda s:  (s.split("=")[0][-1], int(s.split("=")[1]))	
	for sym in syms:
		f = decode_sym( sym )
		print(f"Apply symmetry {f}")
		xy = 0 if f[0]=="x" else 1
		# create list of remaining points, before symmetry
		new_points = []
		for point in points:
			if point[xy] < f[1]:
				new_points.append( point )
		# apply symmetry on the other points
		for point in points:
			if point[xy] > f[1]:
				s = lambda x: 2*f[1]-x
				new_point = [
								point[0] if xy==1 else s(point[0]),
								point[1] if xy==0 else s(point[1])
							]
				if new_point not in new_points:
					new_points.append( new_point )
		points = new_points
		print(f"	now, there are {len(points)} points")
		
	# display the resulting picture
	xmax = 0
	ymax = 0
	for point in points:
		xmax = max(xmax, point[0])
		ymax = max(ymax, point[1])
	for j in range(ymax+1):
		line = ""
		for i in range(xmax+1):
			if [i,j] in points:
				line += "#"
			else:
				line += " "
		print( line )
	
			

main()
