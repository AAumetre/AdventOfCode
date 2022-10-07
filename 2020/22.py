from functions import *

def main():
	logging.basicConfig(level=logging.DEBUG)
	data = read_file("data/22.in")
	
	p1 = []
	p2 = []
	for line in data:
		if "Player 1" in line:
			deck = p1
		elif "Player 2" in line:
			deck = p2
		elif line == "":
			continue
		else:
			deck.append(int(line))
	logging.debug(f"\tPlayer 1's deck is: {p1}\n\t\tPlayer 2's deck is: {p2}")
	
	# play the game
	while p1 != [] and p2 != []:
		if p1[0] > p2[0]:
			p1.append(p1[0])
			p1.append(p2[0])
		else:
			p2.append(p2[0])
			p2.append(p1[0])
		del p1[0]
		del p2[0]
	logging.debug(f"\tPlayer 1's deck is: {p1}\n\t\tPlayer 2's deck is: {p2}")
	
	# compute score
	if p1 == []:
		winner = p2
	else:
		winner = p1
	scoring_list = [(len(winner)-i)*winner[i] for i in range(len(winner))]
	logging.info(f"The score of the winning player is {sum(scoring_list)}")
	

start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns()-start_time) / 10 ** 9} s")
