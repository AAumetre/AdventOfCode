from functions import *
from typing import List
from typing import Callable
from typing import Tuple
from typing import Union
import numpy as np

class BitsParser:
	def __init__(self, buff: str):
		self.buff = buff
		self.index = 0
		self.versions = []

	def read_bits(self, n: int) -> int:
		val = int(self.buff[self.index:self.index+n], 2)
		self.index += n
		return val

	def read_chars(self, n: int) -> str:
		ret = self.buff[self.index:self.index+n]
		self.index += n
		return ret

	def process_operator_length(self, length: int, type: int) -> int:
		end = self.index + length
		values = []
		while self.index < end:
			values.append( self.process_packet() )
		return self.evaluate(values, type)

	def process_operator_count(self, count: int, type: int) -> int:
		values = []
		for c in range(count):
			values.append(self.process_packet())
		return self.evaluate(values, type)

	def process_literal_value(self) -> int:
		done = False
		string = ""
		while not done:
			next = self.read_chars(5)
			if next[0] == "0":
				done = True
			string += next[1:]
		return int(string, 2)

	def process_packet(self) -> int:
		if self.index+6 > len(self.buff)-1:
			print(f"	not enough bits to read anymore")
			return 0
		version = self.read_bits(3)
		type_id = self.read_bits(3)
		self.versions.append(version)

		if type_id == 4: # literal value
			return self.process_literal_value()
		else: # operators
			length_type_id = self.read_bits(1)
			if length_type_id == 0:
				sub_packets_length = self.read_bits(15)
				return self.process_operator_length(sub_packets_length, type_id)
			else:
				sub_packets_count = self.read_bits(11)
				return self.process_operator_count(sub_packets_count, type_id)

	def evaluate(self, values: List[int], type: int) -> int:
		if type == 0: # sum
			return sum(values)
		elif type == 1: # product
			return np.prod(values)
		elif type == 2: # min
			return min(values)
		elif type == 3: # max
			return max(values)
		elif type == 5: # [0] greater than [1]
			return values[0] > values[1]
		elif type == 6: # [0] less than [1]
			return values[0] < values[1]
		elif type == 7: # equal
			return values[0] == values[1]
		else:
			print(f"ERROR: unexpected packet type ID: {type}")
			return 0


def main():
	data = read_file("16.in")[0]
	bin_buffer = ""
	for h in data:
		bin_buffer += bin(int(h, 16)).replace("0b","").zfill(4)

	bp = BitsParser(bin_buffer)
	out = bp.process_packet()
	print(f"The sum of all the versions is equal to {sum(bp.versions)}")
	print(f"The evaluation of the expression gives {out}")
main()
