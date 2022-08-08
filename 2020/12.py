from functions import *

def part1(data: List[str]) -> None:

    position = [0, 0]
    heading = 0
    for line in data:
        order = line[0]
        value = int(line[1:])
        if order in ["L", "R"]:
            angle = value if order == "L" else -value
            heading = (heading + angle)%360
        elif order == "N":
            position[1] += value
        elif order == "S":
            position[1] -= value
        elif order == "E":
            position[0] += value
        elif order == "W":
            position[0] -= value
        elif order == "F":
            angle = heading * math.pi / 180
            position[0] += value*math.cos(angle)
            position[1] += value*math.sin(angle)
    logging.info(f"The distance from the start position is {int(abs(position[0])+abs(position[1]))}")

def part2(data: List[str]) -> None:
    position = [0, 0]
    waypoint = [10, 1]
    for line in data:
        order = line[0]
        value = int(line[1:])
        if order in ["L", "R"]:
            distance = math.sqrt(waypoint[0]**2 + waypoint[1]**2)
            heading = math.acos(waypoint[0]/distance)
            if math.sin(waypoint[1]/distance) < 0:
                heading *= -1
            angle = (value if order == "L" else -value)*math.pi/180
            heading += angle
            waypoint[0] = math.cos(heading)*distance
            waypoint[1] = math.sin(heading)*distance
        elif order == "N":
            waypoint[1] += value
        elif order == "S":
            waypoint[1] -= value
        elif order == "E":
            waypoint[0] += value
        elif order == "W":
            waypoint[0] -= value
        elif order == "F":
            position[0] += value*waypoint[0]
            position[1] += value*waypoint[1]
    logging.info(f"The distance from the start position is {int(abs(position[0])+abs(position[1]))}")

def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/12.in")
    part1(data)
    part2(data)



main()