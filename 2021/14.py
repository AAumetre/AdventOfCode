from functions import *

def get_new_pairs(pair: str, transfo: dict) -> List[str]:
	first = pair[0]+transfo[pair]
	second = transfo[pair]+pair[1]
	return [first, second]

def main():
	data = read_file("14.in")
	polymer = data[0]
	insert_between = {pair.split(" -> ")[0]: pair.split(" -> ")[1] for pair in data[2:]}
	
	polymer_chains = [polymer[i]+polymer[i+1] for i in range(len(polymer)-1)]
	chains = {k: 0 for k,v in insert_between.items()}
	for chain in polymer_chains:
		chains[chain] += 1
	
	for t in range(40):
		new_chains = {k: 0 for k,v in insert_between.items()}
		for chain in [c for c in chains if chains[c]>0]:
			new_pair = get_new_pairs(chain, insert_between)
			new_chains[new_pair[0]] += chains[chain]
			new_chains[new_pair[1]] += chains[chain]
		chains = new_chains
	
	letters = {}
	for pair in chains:
		for c in pair:
			if c not in letters:
				letters[c] = chains[pair]
			else:
				letters[c] += chains[pair]
	rev = {v: k for k,v in letters.items()} # reverse the dictionary
	print(f"The difference is 1+{max(rev)//2}-{min(rev)//2}={1+max(rev)//2-min(rev)//2}")
		

main()
