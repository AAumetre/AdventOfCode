from functions import *

Node = typing.NewType("Node", None)


@dataclass()
class Node:
	parent_: Node
	children_: Dict[str, Node]
	size_: int
	

def get_size(node_: Node) -> int:
	""" Computes the size of a node, as per  AoC definition. """
	if node_.children_ == {}:
		return node_.size_
	else:
		total_size = 0
		for _, c in node_.children_.items():
			total_size += get_size(c)
		node_.size_ = total_size
		return total_size
		

def get_dir_sizes(node_: Node) -> List[int]:
	""" Browses a graph and returns the list of all the dir's sizes. """
	if node_.children_ == {}:
		return []
	else:
		size = [node_.size_]
		for _, c in node_.children_.items():
			size += get_dir_sizes(c)
		return size
	

def main():
	logging.basicConfig(level=logging.INFO)
	data = read_file("data/07.in")

	root = Node(None, {}, 0)
	current_node = root
	for line in data:
		logging.debug(f">>>> {line}.")
		if line[:4] == "$ cd":
			if line[5:] == "/":
				current_node = root
			elif line[5:] == "..":
				current_node = current_node.parent_
			else:
				current_node = current_node.children_[line[5:]]
		elif line[:4] == "$ ls":
			pass
		else:  # we're inside an 'ls' output
			if line[:3] == "dir":
				current_node.children_[line[4:]] = Node(current_node, {}, 0)
			else:
				current_node.children_[line.split()[1]] = Node(current_node, {}, int(line.split()[0]))
	
	used_space = get_size(root)  # updates directory sizes
	dir_sizes = sorted(get_dir_sizes(root))
	small_dir_size = sum([s for s in dir_sizes if s < 100000])
	logging.info(f"The size of all the small directories is {small_dir_size}.")
	
	target_space = used_space + 30000000 - 70000000
	smallest_dir = min([d for d in dir_sizes if d >= target_space])
	logging.info(f"The smallest dir that we should remove is of size {smallest_dir}.")
	
	

start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
