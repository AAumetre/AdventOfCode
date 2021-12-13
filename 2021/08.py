from functions import *



def main(): # Seven-digit display
	data = transform(lambda x: transform(lambda y: y.split(" "), x.split(" | ")), read_file("08.in"))
	out = list(itertools.chain(*[line[1] for line in data]))
	print( sum(transform(lambda x: 1 if len(x)==2 or len(x)==3 or len(x)==4 or len(x)==7 else 0, out)) )
	
	sum_all = 0
	for line in data:
		numbers = line[0]
		# decode
		table = {"a":"x", "b":"x", "c":"x", "d":"x", "e":"x", "f":"x", "g":"x"}
		# frequency analysis
		frequencies = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0}
		for number in numbers:
			for letter in number:
				frequencies[letter] += 1
		table["b"] = [b_ for b_ in frequencies if frequencies[b_] == 6][0]
		table["e"] = [b_ for b_ in frequencies if frequencies[b_] == 4][0]
		table["f"] = [b_ for b_ in frequencies if frequencies[b_] == 9][0]
		# deduction
		one = [one for one in numbers if len(one) == 2][0]
		four = [four for four in numbers if len(four) == 4][0]
		seven = [seven for seven in numbers if len(seven) == 3][0]
		eight = [eight for eight in numbers if len(eight) == 7][0]
		table["c"] = remove_chars(one, [table["f"]]) # number 1 is cf, we already know f		
		table["a"] = remove_chars(seven, [table["f"],table["c"]]) # number 7 is acf, we already know c and f
		table["d"] = remove_chars(four, [table["b"],table["f"],table["c"]])  # number 4 is bcdf, we already know b, c and f
		table["g"] = remove_chars(eight, [table["a"],table["b"],table["c"],table["d"],table["e"],table["f"]])  # number 8 is abcdefg, we already know a, b, c, d, e and f
		# compute the output
		out = line[1]
		num = []
		for digit in out:
			tr_digit = []
			for char in digit:
				tr_digit.append( [tr_char for tr_char in table if table[tr_char]==char][0] )
			num.append( decode_7seg(tr_digit) )
		# accumulate
		sum_all += 1000*num[0] + 100*num[1] + 10*num[2] + num[3]
	print(f"The whole sum is equal to {sum_all}")
	
	

main()
