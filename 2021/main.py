

def disp_data(data):
    for l in data:
        print([e for e in l] )

def neighbors(data, i, j):
    neighbors = []
    if i-1 >= 0:
        neighbors.append([i-1,j])
        if j-1 >= 0:
            neighbors.append([i-1,j-1])
        if j+1 < len(data):
            neighbors.append([i-1,j+1])
    if i+1 < len(data[0]):
        neighbors.append([i+1,j])
        if j-1 >= 0:
            neighbors.append([i+1,j-1])
        if j+1 < len(data):
            neighbors.append([i+1,j+1])
    if j-1 >= 0:
        neighbors.append([i,j-1])
    if j+1 < len(data):
        neighbors.append([i,j+1])
    return neighbors


def main():
    data = []
    for l in open("11.in", "r"):
        data.append( [int(_) for _ in l.strip()] )

    flash = 0
    for t in range(2000):
        done = False
        for j in range(len(data)):
            for i in range(len(data[0])):       
                data[j][i] += 1
        while not done:        
            done = True
            update = [ [0]*len(data[0]) for i in range(len(data))]
            for j in range(len(data)):
                for i in range(len(data[0])):
                    if data[j][i] > 9:
                        done = False
                        for n in neighbors(data, i, j):
                            update[ n[1] ][ n[0] ] += 1
                        data[j][i] = 0
                        flash += 1
            # Update once all are analyzed
            for j in range(len(data)):
                for i in range(len(data[0])):
                    if data[j][i] != 0:
                        data[j][i] += update[j][i]
        if sum([sum(line) for line in data]) == 0:
            print(f"At t={t+1}, all octopuses flash")
            exit(1)
    print(f"There has been {flash} flashes")



if __name__ == "__main__":
    main()
