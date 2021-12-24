from functions import *


def replace_i(number: str, digit: str, index: int) -> str:
	return number[:index] + digit + number[index+1:]
	
def get_prev(number: str, index: int) -> str:
	n = int(number[index]) - 1
	if n == 0:
		number = replace_i(number, "9", index)
		return get_prev(number, index-1)
	else:
		return replace_i(number, str(n), index)
		
def f(w, z, a, b, c) -> int:
	x = not( (z%26+b) == w)
	return (z//a)*(25*x+1)+x*(w+c)

def main():
	data = read_file("24.in")
	instructions = [line.split(" ") for line in data]
	
	
	parameters = []
	for i in range(len(data)//18):
		a = int(instructions[18*i + 4][2])
		b = int(instructions[18*i + 5][2])
		c = int(instructions[18*i + 15][2])
		parameters.append( [a,b,c] )	
	
	model_number = "13579246899999"
	z = 0
	input_index = 0
	for param_set in parameters:
		w = int(model_number[input_index])
		input_index += 1
		z = f(w, z, param_set[0], param_set[1], param_set[2])
	print(f"Final value for z is {z}")
	
	model_number = "99999999999999" #14-digit input number
	highest_model_number = ""	
	cnt = 0
	while True:
		model_number = get_prev(model_number, 13)
		z = 0
		input_index = 0
		cnt += 1
		if cnt%1000 == 0:
			print(f"Testing {model_number}")
		for param_set in parameters:
			w = int(model_number[input_index])
			input_index += 1
			z = f(w, z, param_set[0], param_set[1], param_set[2])
		if z == 0:
			print(f"New model number found! {model_number}")
			exit(0)
	
			
		
		
	
	model_number = "99999999999999" #14-digit input number
	highest_model_number = ""
	registers = {"x": 0, "y": 0, "z": 0, "w": 0}
	
	cnt = 0
	while highest_model_number == "":
		model_number = get_prev(model_number, 13)
		cnt += 1
		input_index = 0
		if cnt%1000 == 0:
			print(f"Testing {model_number}")
		for ins in instructions:
			# print(f"{ins}\t\t{registers}")
			if ins[0] == "inp":
				registers[ins[1]] = int(model_number[input_index])
				input_index += 1
			elif ins[0] == "add":
				if ins[2] in registers:
					registers[ins[1]] += registers[ins[2]]
				else:
					registers[ins[1]] += int(ins[2])
			elif ins[0] == "mul":
				if ins[2] in registers:
					registers[ins[1]] *= registers[ins[2]]
				else:
					registers[ins[1]] *= int(ins[2])
			elif ins[0] == "div":
				if ins[2] in registers:
					registers[ins[1]] //= registers[ins[2]]
				else:
					registers[ins[1]] //= int(ins[2])
			elif ins[0] == "mod":
				if ins[2] in registers:
					registers[ins[1]] %= registers[ins[2]]
				else:
					registers[ins[1]] %= int(ins[2])
			elif ins[0] == "eql":
				if ins[2] in registers:
					registers[ins[1]] = (registers[ins[1]] == registers[ins[2]])
				else:
					registers[ins[1]] = (registers[ins[1]] == int(ins[2]))
			else:
				print(f"ERROR decoding instruction {ins}")
				exit(1)
		# print(f"Program stopped, register values are:\n{registers}")
		if registers["z"] == 0:
			print(f"New model number found! {model_number}")
			highest_model_number = model_number
			exit(0)


main()
