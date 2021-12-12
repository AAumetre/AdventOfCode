
def find_path(path, neighbors, paths_found):
    current_node = path[-1]
    for n in neighbors[current_node]:
        if n == "end":
            path.append(n)
            paths_found.append( path )
            continue
        if n.islower() and n in path:
            continue # small cave already visited
        else:
            possible_path = path.copy()
            possible_path.append(n)
            find_path(possible_path, neighbors, paths_found)
    return paths_found

def main():
    links = []
    for line in open("12.in", "r"):
        links.append( line.strip().split("-") )

    neighbors = {}
    for link in links:
        if link[0] not in neighbors:
            neighbors[ link[0] ] = [ link[1] ]
        else:
            neighbors[ link[0] ].append( link[1] )
        if link[1] not in neighbors:
            neighbors[ link[1] ] = [ link[0] ]
        else:
            neighbors[ link[1] ].append( link[0] )

    print( len(find_path(["start"], neighbors, [])) )


main()