from functions import *



def main(): # Height-map
	data = transform(lambda x: [int(_) for _ in x], read_file("09.in"))
	risk = 0
	minima = []
	for j in range(len(data)):
		for i in range(len(data[0])):
			curr = data[j][i]
			for n in get_neigh(i, j, len(data[0]), len(data)):
				if data[n[1]][n[0]] <= curr:
					curr = -1
			if curr != -1:
				minima.append( [i,j] )
			risk += (1+curr)
	print(f"Total risk is {risk}")
	
	basin = [[0 for j in range(len(data))] for i in range(len(data[0]))]
	basin_sizes = []
	for start in minima:
		basin_size = 0
		to_explore = [start]
		while len(to_explore) > 0:
			for point in to_explore:
				for neigh in get_neigh(point[0], point[1], len(data[0]), len(data)):
					i = neigh[0]
					j = neigh[1]
					if (data[j][i] < 9) and ( basin[i][j] != 1 ):
						basin[i][j] = 1
						basin_size += 1
						to_explore.append( [i,j] )
				to_explore.remove( point )
		basin_sizes.append( basin_size )
	
	three_largest = functools.reduce(lambda x,y: x*y, sorted(basin_sizes)[-3:])
	print(f"The product of the sizes of the three largest basins is {three_largest}")

	

main()
