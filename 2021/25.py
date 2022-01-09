from functions import *
import copy

def render(cucumbers) -> str:
    ret = ""
    for j in range(len(cucumbers)):
        line = ""
        for i in range(len(cucumbers[0])):
            line += cucumbers[j][i]
        line += "\n"
        ret += line
    return ret

def main():
    data = read_file("25.in")
    cucumbers = {}
    for j in range(len(data)):
        cucumbers[j] = {}
        for i in range(len(data[0])):
            cucumbers[j][i] = data[j][i]

    print(render(cucumbers))
    stable = False
    step_counter = 0
    while not stable:
        stable = True
        new_cucumbers = copy.deepcopy(cucumbers)
        for j in range(len(data)):
            for i in range(len(data[0])):
                if i != len(data[0])-1:
                    next_east = i + 1
                else:
                    next_east = 0
                if cucumbers[j][i]==">" and cucumbers[j][next_east] == ".":
                    new_cucumbers[j][i] = "."
                    new_cucumbers[j][next_east] = ">"
                    stable = False
        cucumbers = new_cucumbers
        new_cucumbers = copy.deepcopy(cucumbers)
        for j in range(len(data)):
            if j != len(data)-1:
                next_south = j + 1
            else:
                next_south = 0
            for i in range(len(data[0])):
                if cucumbers[j][i]=="v" and cucumbers[next_south][i] == ".":
                    new_cucumbers[j][i] = "."
                    new_cucumbers[next_south][i] = "v"
                    stable = False
        cucumbers = new_cucumbers
        step_counter += 1
    print(step_counter)
    print(render(cucumbers))


main()