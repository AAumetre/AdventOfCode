from functions import *
import math
import logging

class Leaf:
    value: int
    parent: Union['Node', None]
    depth: int

    def __init__(self, number: int, parent: 'Node' = None):
        if parent is None: # Starting node
            self.parent = None
            self.depth = 0
        else:
            self.parent = parent
            self.depth = parent.depth + 1
        self.value = number


class Node:
    left: Union['Node', 'Leaf', None]
    right: Union['Node', 'Leaf', None]
    parent: Union['Node', None]
    depth: int

    def __init__(self, number: List, parent: 'Node' = None):
        if parent is None: # Starting node
            self.parent = None
            self.depth = 0
        else:
            self.parent = parent
            self.depth = parent.depth + 1
        # Set leaf/node
        if isinstance(number[0], list): # Create a node
            self.left = Node(number[0], self)
        else: # Create a leaf
            self.left = Leaf(number[0], self)
        if isinstance(number[1], list): # Create a node
            self.right = Node(number[1], self)
        else: # Create a leaf
            self.right = Leaf(number[1], self)


def update_depths(number: 'Node', depth: int) -> None:
    """ Makes sure the depth values are up-to-date """
    deeper = depth + 1
    if number.left is not None: number.left.depth = deeper
    if number.right is not None: number.right.depth = deeper
    if isinstance(number.left, Node): update_depths(number.left, deeper)
    if isinstance(number.right, Node): update_depths(number.right, deeper)

def in_order_nodes(top: 'Node') -> List['Node']:
    """ Traverse graph from left to right but only return node list """
    nodes = []
    if isinstance(top.left, Node): nodes += in_order_nodes(top.left)
    nodes += [top]
    if isinstance(top.right, Node): nodes += in_order_nodes(top.right)
    return nodes

def in_order_leaves(top: 'Node') -> List['Leaf']:
    """ Traverse graph from left to right but only return leaf list """
    leaves = []
    if isinstance(top.left, Node):
        leaves += in_order_leaves(top.left)
    else:
        leaves += [top.left]
    if isinstance(top.right, Node):
        leaves += in_order_leaves(top.right)
    else:
        leaves += [top.right]
    return leaves

def render_number(number: 'Node') -> str:
    """ Creates an AoC-like bracket representation of the binary tree """
    line = "["
    if isinstance(number.left, Leaf):
        line += str(number.left.value)
    else:
        line += render_number(number.left)
    line += ","
    if isinstance(number.right, Leaf):
        line += str(number.right.value)
    else:
        line += render_number(number.right)
    line += "]"
    return line

def render_node(node: 'Node') -> str:
    render_left = node.left if isinstance(node.left, Node) else node.left.value
    render_right = node.right if isinstance(node.right, Node) else node.right.value
    return f"[{render_left},{render_right}]"

def rightmost_leaf(top: 'Node') -> 'Leaf':
    if isinstance(top.right, Leaf):
        return top.right
    else:
        return rightmost_leaf(top.right)

def left_leaf(leaf: 'Leaf') -> Union['Leaf', None]:
    """ Find the left neighbor of a given leaf """
    inspected = leaf.parent
    previous = leaf
    while inspected.left == previous: # go up until there is a right node/leaf
        previous = inspected
        if previous.parent is None: return None
        inspected = previous.parent
    inspected = inspected.left
    while not isinstance(inspected, Leaf): # from there, take always right until you find a leaf
        inspected = inspected.right
    return inspected

def right_leaf(leaf: 'Leaf') -> Union['Leaf', None]:
    """ Find the right neighbor of a given leaf """
    inspected = leaf.parent
    previous = leaf
    while inspected.right == previous: # go up until there is a left node/leaf
        previous = inspected
        if previous.parent is None: return None
        inspected = previous.parent
    inspected = inspected.right
    while not isinstance(inspected, Leaf): # from there, take always left until you find a leaf
        inspected = inspected.left
    return inspected

def explode(top: 'Node') -> None:
    # find nodes whose depth = 4
    depth_4_nodes = [node for node in in_order_nodes(top) if node.depth == 4]
    for to_explode in depth_4_nodes:
        logging.debug(f"Node containing {render_node(to_explode)}] needs to explode")
        # explode by adding values left and right
        left_neighbor = left_leaf(to_explode.left)
        if left_neighbor is not None:
            left_neighbor.value += to_explode.left.value
        right_neighbor = right_leaf(to_explode.right)
        if right_neighbor is not None:
            right_neighbor.value += to_explode.right.value
        # replace that node by a 0-Leaf
        zero_leaf = Leaf(0, to_explode.parent)
        if to_explode == to_explode.parent.left: to_explode.parent.left = zero_leaf
        if to_explode == to_explode.parent.right: to_explode.parent.right = zero_leaf

def split(top: 'Node') -> bool:
    to_split = [leaf for leaf in in_order_leaves(top) if leaf.value >= 10]
    if len(to_split) > 0:
        leaf = to_split[0]
        parent = leaf.parent
        new_left = math.floor(leaf.value / 2)
        new_right = math.ceil(leaf.value / 2)
        new_node = Node([new_left, new_right], parent)
        logging.debug(f"\tpair {render_node(parent)}'s {leaf.value} leaf must split into {render_node(new_node)})")
        if leaf == parent.left:
            parent.left = new_node
        else:
            parent.right = new_node
        return True
    return False

def snail_reduce(top: 'Node') -> 'Node':
    """ Reduce a snailfish number and return it """
    a_number_was_split = True
    while a_number_was_split:
        explode(top)
        a_number_was_split = split(top)
    return top

def add(left: 'Node', right: 'Node') -> 'Node':
    """ Add left and right, reduce and return the resulting top node """
    # create new top node
    new_top = Node([0, 0])
    new_top.left = left
    new_top.right = right
    # set former top node's parents to new top_node
    left.parent = new_top
    right.parent = new_top
    # re-compute every depth
    update_depths(new_top, 0)
    # call reduce
    return snail_reduce(new_top)

def magnitude(top: 'Node') -> int:
    """ Compute the magnitude of a snail number """
    if isinstance(top.left, Leaf):
        left_magnitude = top.left.value
    else:
        left_magnitude = magnitude(top.left)
    if isinstance(top.right, Leaf):
        right_magnitude = top.right.value
    else:
        right_magnitude = magnitude(top.right)
    return 3*left_magnitude + 2*right_magnitude



def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("18.in")
    numbers = [eval(e) for e in data]
    start = Node(numbers[0])

    for number in numbers[1:]:
        logging.info(f"Adding {number}")
        new = add(start, Node(number))
        start = new
    logging.info(f"Result of the addition is {render_number(start)}")
    logging.info(f"\t\t its magnitude is {magnitude(start)}")

    max_magnitude = 0
    for n1, n2 in itertools.product(numbers, numbers):
        mag = magnitude(add(Node(n1), Node(n2)))
        max_magnitude = max(mag, max_magnitude)
        mag = magnitude(add(Node(n2), Node(n1)))
        max_magnitude = max(mag, max_magnitude)
    logging.info(f"The maximum magnitude is {max_magnitude}")



main()