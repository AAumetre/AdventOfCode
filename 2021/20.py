from functions import *
from typing import Dict

Image = List[str]

def get_enhanced(algo: str) -> Dict[str, str]:
	""" From the 'algorithm', builds a dict returning the new pixel,
		based on its surroundings """
	table = {}
	for i in range(2**9):
		i_str = bin(i)[2:].zfill(9).replace("0", ".").replace("1", "#")
		table[i_str] = algo[i]
	return table
	
def widen(image: Image, char: str) -> Image:
	""" Adds characters around an image """
	top_line = char*(len(image[0])+4)
	new_image = [top_line, top_line]
	for line in image:
		new_line = char + char + line + char + char
		new_image.append(new_line)
	new_image.append(top_line)
	new_image.append(top_line)
	return new_image

def extract(image: Image, pi: int, pj: int) -> str:
	""" Extract the 'pixels' surrounding an (i,j) pixel.
		!!! Does not do boundary checks !!! """
	line = ""
	for j in [pj-1, pj, pj+1]:
		line += image[j][pi-1:pi+2]
	return line

def render(image: Image) -> str:
	""" Creates one string to be printed """
	ret = ""
	for j in range(len(image)):
		ret += "\n"
		for i in range(len(image[0])):
			ret += image[j][i]
	ret += "\n"
	return ret

def main(n_repeats: int):
	data = read_file("20.in")
	algo = data[0]
	image_str = data[2:]
	image = []
	for line in image_str:
		image.append(line)
	
	table = get_enhanced(algo)
	
	inf_char = "."
	for _ in range(n_repeats):
		image = widen(image, inf_char)
		new_image = []
		for j in range(1, len(image)-1):
			line = ""
			for i in range(1, len(image[0])-1):
				new_char = table[extract(image, i, j)]
				line += new_char
			new_image.append(line)
		image = new_image
		inf_char = table[inf_char*9]

	counter = 0
	for j in range(len(image)):
		for i in range(len(image[0])):
			if image[j][i] == "#": counter += 1
	print(counter)

main(2)
main(50)
