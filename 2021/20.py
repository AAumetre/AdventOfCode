from functions import *

Picture = List[str]

def get_three_lines(i: int, j:int, I: int, J:int) -> List[List[int]]:
    """ Format is [j, i-start, i-end] """
    three_lines = []
    if j-1 >= 0:
        line1 = [j-1, i, i+1]
        if i-1 >= 0:
            line1[1] = i-1
        if i+1 >= I:
            line1[2] = i
        three_lines.append(line1)
    line2 =  [j, i, i+1]
    if i-1 >= 0:
        line2[1] = i-1
    if i+1 >= I:
        line2[2] = i
    three_lines.append(line2)
    if j+1 < J:
        line3 =  [j+1, i, i+1]
        if i-1 >= 0:
            line3[1] = i-1
        if i+1 >= I:
            line3[2] = i
        three_lines.append(line3)
    return three_lines

def create_empty_picture(I: int, J: int) -> Picture:
    new_pic = []
    line = []
    for i in range(I):
        line.append(".")
    for j in range(J):
        new_pic.append(line)
    return new_pic

def enhance(pic: Picture, algo: str) -> Picture:
    J = len(pic)
    I = len(pic[0])
    new_pic = create_empty_picture(I, J)
    for j in range(J):
        for i in range(I):
            number_str = ""
            for l in get_three_lines(i, j, I, J):
                number_str +=  pic[l[0]][l[1]:l[2]+1]
            number_str = number_str.replace("#", "1")
            number_str = number_str.replace(".", "0")
            index = int(number_str,2)
            new_pic[j][i] = algo[index]
    return pic





def print_picture(pic: Picture) -> None:
    for l in pic:
        print(l)

def main():
    data = read_file("data/20.ex")
    algorithm = data[0]
    picture = []
    for line in data[2:]:
        picture.append(line)

    print_picture(picture)
    picture = enhance(picture, algorithm)
    print_picture(picture)




main()