from functions import *

def count_bags(from_bag: str, bag_contains: Dict) -> int:
    sum = 0
    for count, bag in bag_contains[from_bag]:
        sum += count*(1+count_bags(bag, bag_contains))
    return sum

def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/07.in")
    bag_contains = defaultdict(list)
    contained_by = defaultdict(set)
    for rule in data:
        split = rule.split(" bags contain ")
        bag = split[0]
        if "no other bags" not in split[1]:
            for contained in split[1].split(", "):
                count = int(contained[0])
                color = contained[2:].split(" bag")[0]
                bag_contains[bag].append((count, color))
                contained_by[color].add(bag)
        logging.debug(f"\trule for bag {bag} is: {[rule for rule in bag_contains[bag]]}")

    container_bags = set({})
    bags_to_contain = ["shiny gold"]
    while bags_to_contain:
        bag = bags_to_contain.pop()
        for container in contained_by[bag]:
            container_bags.add(container)
            bags_to_contain.append(container)
    logging.debug(f"Set containing shiny gold: {container_bags}")
    logging.info(f"The number of bags containing shiny gold is {len(container_bags)}.")

    number_of_bags = count_bags("shiny gold", bag_contains)
    logging.info(f"The number of bags a shiny gold bag must contain is {number_of_bags}.")


main()