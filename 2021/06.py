from functions import *



def main(): # Lantern-fish
	fish = list(map( lambda x: int(x), read_file("06.in")[0].replace("\n", "").split(",")))
		
	adult_fish = [0, 0, 0, 0, 0, 0, 0, 0] # number of fish, sorted by remaining days
	child_fish = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # number of fish, sorted by remaining days
	for f in fish:
		adult_fish[f] += 1
	for i in range(256):
		new_child_fish = adult_fish[0] + child_fish[0]
		adult_fish[7] = new_child_fish
		child_fish[9] = new_child_fish
		adult_fish = adult_fish[1:]
		child_fish = child_fish[1:]
		adult_fish.append(0)
		child_fish.append(0)
	n_fish = sum(adult_fish) + sum(child_fish)	
	print(f"There are {n_fish} fish in the sea")
	

main()
