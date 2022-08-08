from functions import *

def encountered_tree(ski_slope: List[str], slope: List[int]) -> int:
    tree_count = 0
    pos = [0, 0]
    while pos[1] < len(ski_slope)-1:
        pos[0] += slope[0]
        pos[1] += slope[1]
        if pos[0] > len(ski_slope[0])-1:
            pos[0] -= len(ski_slope[0])
        if ski_slope[pos[1]][pos[0]] == "#":
            tree_count += 1
    return tree_count

def main():
    logging.basicConfig(level=logging.INFO)
    ski_slope = read_file("data/03.in")
    print(encountered_tree(ski_slope, [3,1]))
    print(encountered_tree(ski_slope, [1,1])*
          encountered_tree(ski_slope, [3,1])*
          encountered_tree(ski_slope, [5,1])*
          encountered_tree(ski_slope, [7,1])*
          encountered_tree(ski_slope, [1,2]))
main()