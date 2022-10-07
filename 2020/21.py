from functions import *

def main():
	logging.basicConfig(level=logging.DEBUG)
	data = read_file("data/21.in")
	
	allergen_dict = {} # name: set(ingredients)
	all_ingredients = defaultdict(int) # ingredient: count, default value is 0
	for line in data:
		ingredients = set(line.split(" (contains ")[0].split(" "))
		for ingredient in ingredients:
			all_ingredients[ingredient] += 1
		allergens = line.split(" (contains ")[1][:-1].split(", ")
		for allergen in allergens:
			if allergen in allergen_dict:
				allergen_dict[allergen] = allergen_dict[allergen].intersection(ingredients)
			else:
				allergen_dict[allergen] = ingredients
	logging.debug(f"{allergen_dict=}")
	non_allergenic = all_ingredients.copy()
	for _, allergen_set in allergen_dict.items():
		for allergen in allergen_set:
			if allergen in non_allergenic:
				del non_allergenic[allergen]
	count = sum(non_allergenic.values())
	logging.info(f"The number of occurences of non-allergenic ingredients is {count}.")
	
	
	# clean the dict, until there's a bijection between ingredients and allergens
	cleaned_allergen_dict = {}
	done = False
	while not done:
		done = True
		for allergen, ingredients in allergen_dict.items():
			if len(ingredients) == 1:
				done = False
				found_ingredient = ingredients.pop()
				# store it
				cleaned_allergen_dict[allergen] = found_ingredient
				# then, remove it from the other allergens possibilities
				for other_allergen, other_ingredients in allergen_dict.items():
					if found_ingredient in other_ingredients:
						other_ingredients.remove(found_ingredient)
				del allergen_dict[allergen]
				break
	logging.debug(f"{cleaned_allergen_dict=}")

	sorted_ingredients = []
	sorted_allergens = sorted(list(cleaned_allergen_dict))
	print(sorted_allergens)
	for allergen in sorted_allergens:
		sorted_ingredients.append(cleaned_allergen_dict[allergen])
	canonical_list = ",".join(sorted_ingredients)
	logging.info(f"The canonical dangerous ingredients list is \"{canonical_list}\".")

start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns()-start_time) / 10 ** 9} s")
