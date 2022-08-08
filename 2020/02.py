from functions import *

def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/02.in")
    valid_p1 = 0
    valid_p2 = 0
    for line in data:
        s_line = line.split(": ")
        password = s_line[1]
        s_line = s_line[0].split(" ")
        letter = s_line[1]
        s_line = s_line[0].split("-")
        n1 = int(s_line[0])
        n2 = int(s_line[1])
        occurences = 0
        # part 1
        for c in password:
            if c == letter:
                occurences += 1
        if occurences >= n1 and occurences <= n2:
            valid_p1 += 1
        # part 2
        pos1 = (password[n1-1] == letter)
        pos2 = (password[n2-1] == letter)
        if (pos1 ^ pos2):
            valid_p2 += 1
    print(valid_p1, valid_p2)

main()