from functions import *



def main(): # Syntax Error!
	data = read_file("10.in")
	openings = {"(": ")", "[": "]", "{": "}", "<": ">"}
	closings = {v: k for k,v in openings.items()} # reverse the dictionary
	points = {")": 3, "]": 57,  "}": 1197, ">": 25137}
	points2 = {")": 1, "]": 2,  "}": 3, ">": 4}
	
	s_score = 0
	a_scores = []
	for line in data:
		stack = []
		syntax_error = False
		for char in line:
			if char in openings:
				stack.append( char )
			elif stack[-1]==closings[char]:
				stack.pop()
			else: # part 1
				s_score += points[char]
				syntax_error = True
				break
		if not syntax_error: # part 2
			a_score = 0
			for char in list(reversed(stack)):
				a_score *= 5
				a_score += points2[openings[char]]
			a_scores.append( a_score )
	print(f"Syntax checking score: {s_score}")
	print(f"Autocompletion score: {sorted(a_scores)[len(a_scores)//2]}")
	
	

main()
