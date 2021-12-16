from functions import *


def read_bits(buff: str, index: int, n: int) -> Tuple[int, int]:
	val = int(buff[index:index+n], 2)
	index += n
	return val, index


def process_operator_length(buff: str, index: int, length: int) -> Tuple[List[int], int]:
	print(f"Process operator, {length} bits to read:")
	all_versions = []
	end = index + length
	while index < end:
		versions, index = process_packet(buff, index)
		all_versions += versions
		print(f"	versions: {versions}")
	return all_versions, index
	
def process_operator_count(buff: str, index: int, count: int) -> Tuple[List[int], int]:
	print(f"Process operator, {count} packets to read:")
	all_versions = []
	for c in range(count):
		versions, index = process_packet(buff, index)
		all_versions += versions
	return all_versions, index


def process_literal_value(buff: str, index: int) -> Tuple[int, int]:
	print("Process literal value:")
	done = False
	val = 0
	while not done:
		next, index = read_bits(buff, index, 5)
		print(f"	{bin(next)}")
		if next >> 4 == 0:
			done = True
	return 0, index
	
def process_packet(buff: str, index: int) -> Tuple[List[int], int]:
	if index+6 > len(buff)-1:
		print(f"	not enough bits to read anymore")
		return (0, len(buff)-1)
	version, index = read_bits(buff, index, 3)
	type_id, index = read_bits(buff, index, 3)
	all_versions = [version]
	print(f"version '{version}', type ID '{type_id}'")
	
	versions = []
	if type_id == 4: # literal value
		val, index = process_literal_value(buff, index)
	else: # operator
		length_type_id, index = read_bits(buff, index, 1)
		if length_type_id == 0:
			sub_packets_length, index = read_bits(buff, index, 15)
			versions, index = process_operator_length(buff, index, sub_packets_length)
		else:		
			sub_packets_count, index = read_bits(buff, index, 11)
			versions, index = process_operator_count(buff, index, sub_packets_count)
	
	all_versions += versions
	return all_versions, index



def main():
	data = read_file("16.in")[0]
	# packet: [version(3 bits)][type ID(3 bits)]
	# ID 4: literal value, padded with leading zeros to get 4 bits blocks
	#		each group prefixed with 1, except the last one
	print(data)
	
	bin_buffer = ""
	for h in data:
		bin_buffer += bin(int(h, 16)).replace("0b","").zfill(4)
	print( bin_buffer )
	
	index = 0
	all_versions = []
	#while index < len(bin_buffer)-1:
	#	print(f"Starting a new reading from index={index} (over a total length of {len(bin_buffer)})")
	#	versions, index = process_packet(bin_buffer, index)
	#	print(f"All versions (in part): {versions}")
	#	if versions != 0:
	#		all_versions += versions
	all_versions, index = process_packet(bin_buffer, index)
	
	# add all the version numbers
	print(f"The sum of {all_versions} is {sum(all_versions)}")

main()
