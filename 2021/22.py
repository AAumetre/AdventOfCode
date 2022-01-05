from functions import *
from itertools import product


def part1(reboot):
	reactor = {}
	count = 0
	for step in reboot:
		state = step[0]
		rangex = list(range(step[1][0][0], step[1][0][1]+1))
		rangey = list(range(step[1][1][0], step[1][1][1]+1))
		rangez = list(range(step[1][2][0], step[1][2][1]+1) )
		for key in product(rangex, rangey, rangez):
			if reactor.get(key, False) and state is False:
				count -= 1
			elif not reactor.get(key, False) and state is True:
				count += 1
			reactor[key] = state
	print(f"The total number of blocks is {count}")
	
def cut_block(base_block, kernel_block) -> List:
	""" Cut-out a base_block, based on the kernel_block and return
		the list of the 27 resulting blocks, including the kernel_block """
	# X1, x1, x2, X2
	Xs = [base_block[0][0], kernel_block[0][0], kernel_block[0][1], base_block[0][1]]
	# Y1, y1, y2, Y2
	Ys = [base_block[1][0], kernel_block[1][0], kernel_block[1][1], base_block[1][1]]
	# Z1, z1, z2, Z2
	Zs = [base_block[2][0], kernel_block[2][0], kernel_block[2][1], base_block[2][1]]
	pairsX = [(Xs[0],Xs[1]),(Xs[1],Xs[2]),(Xs[2],Xs[3])]
	pairsY = [(Ys[0],Ys[1]),(Ys[1],Ys[2]),(Ys[2],Ys[3])]
	pairsZ = [(Zs[0],Zs[1]),(Zs[1],Zs[2]),(Zs[2],Zs[3])]
	all_blocks = list(product(pairsX, pairsY, pairsZ))
	# Remove zero-width and invalid blocks
	blocks = []
	for block in all_blocks:
		valid = True
		for pair in block:
			if pair[0]==pair[1]:
				valid = False
				break
		if valid:
			blocks.append(block)
	return blocks
	
def patch_blocks(blocks_: List) -> List:
	""" Try patching blocks together, to form a shorter list of larger blocks """
	if len(blocks_) == 0: return []
	blocks = blocks_.copy()
	done = False
	while not done:
		done = True
		for block in blocks:
			patch_made = False
			for other_block in blocks:
				if other_block == block: continue
				# x and y match, glue on z
				if other_block[0]==block[0] and other_block[1]==block[1] and (other_block[2][1]==block[2][0] or other_block[2][0]==block[2][1]):
					z1 = min(block[2][0], block[2][1], other_block[2][0], other_block[2][1])
					z2 = max(block[2][0], block[2][1], other_block[2][0], other_block[2][1])
					new_blocks = blocks.copy()
					new_blocks.remove(block)
					new_blocks.remove(other_block)
					new_blocks.append( (block[0], block[1], (z1, z2)) )
					patch_made = True
				# y and z match, glue on x
				elif other_block[1]==block[1] and other_block[2]==block[2] and (other_block[0][1]==block[0][0] or other_block[0][0]==block[0][1]):
					x1 = min(block[0][0], block[0][1], other_block[0][0], other_block[0][1])
					x2 = max(block[0][0], block[0][1], other_block[0][0], other_block[0][1])
					new_blocks = blocks.copy()
					new_blocks.remove(block)
					new_blocks.remove(other_block)
					new_blocks.append( ((x1, x2), block[1], block[2]) )
					patch_made = True
				# z and x match, glue on y
				elif other_block[2]==block[2] and other_block[0]==block[0] and (other_block[1][1]==block[1][0] or other_block[1][0]==block[1][1]):
					y1 = min(block[1][0], block[1][1], other_block[1][0], other_block[1][1])
					y2 = max(block[1][0], block[1][1], other_block[1][0], other_block[1][1])
					new_blocks = blocks.copy()
					new_blocks.remove(block)
					new_blocks.remove(other_block)
					new_blocks.append( (block[0], (y1, y2), block[2]) )
					patch_made = True
			if patch_made:
				# repeat with the new set of blocks
				blocks = new_blocks.copy()
				done = False
				break
			else:
				# no patch opportunity found for this block
				pass		
	return blocks

def get_intersection(block1, block2) -> Tuple[int, List]:
	""" Returns the size and the intersecting block between two blocks """
	ix = (max(block1[0][0], block2[0][0]), min(block1[0][1], block2[0][1]))
	iy = (max(block1[1][0], block2[1][0]), min(block1[1][1], block2[1][1]))
	iz = (max(block1[2][0], block2[2][0]), min(block1[2][1], block2[2][1]))
	if (ix[0]>ix[1]) or (iy[0]>iy[1]) or (iz[0]>iz[1]):
		return 0, ()
	intersection_block = (ix, iy, iz)
	isize = get_size(intersection_block)
	return isize, intersection_block

def get_size(b) -> int:
	nx = b[0][1]-b[0][0]
	ny = b[1][1]-b[1][0]
	nz = b[2][1]-b[2][0]
	return nx*ny*nz

def is_inside(big_block, small_block) -> bool:
	""" Returns true if the small block is inside the big block """
	isze, iblock = get_intersection(big_block, small_block)
	return iblock == small_block

def part2(reboot):
	# add 1 to each range. For them, 0..0 is of size of, for me 0..1 is
	for step in reboot:
		step[1][0][1] += 1
		step[1][1][1] += 1
		step[1][2][1] += 1
	reactor = {} # {((x1,x2),(y1,y2),(z1,z2)): size}, x2>=x1, etc.
	for step in reboot:
		block_is_on = step[0]
		Xs = (step[1][0][0], step[1][0][1])
		Ys = (step[1][1][0], step[1][1][1])
		Zs = (step[1][2][0], step[1][2][1])
		size = (Xs[1]-Xs[0])*(Ys[1]-Ys[0])*(Zs[1]-Zs[0])
		block = (Xs, Ys, Zs)
		blocks_to_analyse = [block]
		while blocks_to_analyse:
			block = blocks_to_analyse.pop()
			no_intersection = True
			blocks_to_add = []
			blocks_to_delete = []
			for other in reactor:
				isize, intersection_block = get_intersection(block, other)
				if isize > 0:
					no_intersection = False
					if block_is_on: # leave the existing block be, cut yourself
						# create the 27 blocks (tops)
						sub_blocks = cut_block(block, intersection_block)
						# find which are whithin the exisitng one and leave them out
						sub_blocks.remove( intersection_block )
						# try to patch the remaining blocks together to form large blocks
						patched_blocks = patch_blocks( sub_blocks )
						# analyse the resulting blocks, other intersections might occur
						for pb in patched_blocks:
							blocks_to_analyse.append( pb )
						break
					else: # cut the existing block
						blocks_to_delete.append( other )
						if not is_inside(block, other): # else, there is nothing left
							# create the 27 blocks
							sub_blocks = cut_block(other, intersection_block)
							# leave out the one which is whithin the off block
							sub_blocks.remove( intersection_block )
							# try to patch the remaining blocks together to form large blocks
							patched_blocks = patch_blocks( sub_blocks )
							# add them to the reactor: these are known to be valid
							for pb in patched_blocks:
								blocks_to_add.append(pb)
			if no_intersection and block_is_on:
				reactor[block] = get_size(block)
			for block in blocks_to_delete:
				del reactor[block]
			for block in blocks_to_add:
				reactor[block] = get_size(block)
	count = 0
	for block, size in reactor.items():
		count += size
	print(f"The total number of blocks is {count}")



def main():
	data = read_file("22.in")
	reboot = [[line.split(" ")[0]=="on", [[int(number) for number in coord[2:].split("..")] for coord in line.split(" ")[1].split(",")]] for line in data]
	

	# Take only |(x,y)| < 50
	reboot_50 = []
	for step in reboot.copy():
		admissible = True
		for coord in step[1]:
			if abs(coord[0])>50 or abs(coord[1])>50:
				admissible = False
				break
		if admissible:
			reboot_50.append( step )

	part1(reboot_50)
	part2(reboot)

main()