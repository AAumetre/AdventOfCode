from functions import *

def get_next_number(in_: str) -> Tuple[int, str]:
	""" in_ contains only numbers, + and *, no "(" nor ")". """
	indexes = []
	for sign in ["+","*"]:
		idx = in_.find(sign)
		if idx != -1:
			indexes.append(idx)
	if indexes == []:
		end = len(in_)
	else:
		end = min(indexes)
	return (int(in_[:end]), in_[end:])

def compute(in_: str) -> int:
	""" Takes a simple expression and evaluates it.
		in_ contains only numbers, + and *, no "(" nor ")". """
	res, left = get_next_number(in_)
	while left != "":
		operation = left[0]
		num, left = get_next_number(left[1:])
		if operation == "+":
			res += num
		else:
			res *= num
	return res
	
def compute_sums(in_: str) -> str:
	plus_i = in_.find("+")
	if plus_i == -1:
		return in_
	left = re.split("\*|\+", in_[:plus_i])[-1]
	right = re.split("\*|\+", in_[plus_i+1:])[0]
	s = plus_i - len(left)
	e = plus_i + len(right)
	return compute_sums(in_[:s]+str(int(left)+int(right))+in_[e+1:])
	
def weird_compute(in_: str) -> int:
	line = compute_sums(in_)
	# compute product
	res = 1
	for n in line.split("*"):
		res *= int(n)
	return res

def find_closure(in_: str) -> Tuple[int, int]:
	""" Finds the first substring of the form (xxxx) and returns (start, end). """
	first = in_.find("(")
	if first == "-1":
		return (-1, -1)
	while True:
		second = in_.find(")", first)
		if in_.find("(", first+1) != -1:
			first = in_.find("(", first+1)
		else:
			return (first, second)

def reduce_line(in_: str, compute_: Callable) -> str:
	s, e = find_closure(in_)
	if s == -1:
		return in_
	to_compute = in_[s+1:e]
	val = compute_(to_compute)
	line = in_[:s] + str(val) + in_[e+1:]
	return reduce_line(line, compute_)

def main():
	logging.basicConfig(level=logging.INFO)
	data = [line.replace(" ","") for line in read_file("data/18.in")]
	
	acc1 = 0
	acc2 = 0
	for line in data:
		acc1 += int(reduce_line("("+line+")", compute))
		acc2 += int(reduce_line("("+line+")", weird_compute))
	logging.info(f"Part 1: the sum is {acc1}.")
	logging.info(f"Part 2: the sum is {acc2}.")
	

start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns()-start_time) / 10 ** 9} s")
