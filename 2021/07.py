from functions import *



def main(): # Crab-submarines
	pos = transform(lambda x: int(x), read_file("07.in")[0].split(","))
	search_space = [min(pos), max(pos)]
	fuel_consumption = lambda _: fuel_conso(_, pos)
	while search_space[0] != search_space[1]:
		right_target = int((3*search_space[1]+search_space[0])/4)
		right_fuel = fuel_consumption( right_target )
		left_target = int((3*search_space[0]+search_space[1])/4)
		left_fuel = fuel_consumption( left_target )
		if right_fuel < left_fuel:
			search_space[0] = round(0.5*sum(search_space))
		else:
			search_space[1] = round(0.5*sum(search_space))
	print(f"The fuel consumption to reach postion {search_space[0]} is {fuel_consumption(search_space[0])}")

	

main()
