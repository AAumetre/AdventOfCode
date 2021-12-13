from functions import *



def main(): # Submarine dive
	data = read_file( "02.in" )

	forward_list	  = transform( lambda x: int(x), filter_and_remove( data, "forward") )
	up_list			  = transform( lambda x: int(x), filter_and_remove( data, "up") )
	down_list		  = transform( lambda x: int(x), filter_and_remove( data, "down") )

	answer = sum(forward_list)*(sum(down_list)-sum(up_list))
	print(f"The multiplication result is {sum(forward_list)}*({sum(down_list)}-{sum(up_list)})={answer}")

	aim = 0
	f = 0
	d = 0
	for line in data:
		if "forward" in line:
			command_f = int(line.replace("forward", ""))
			f = f + command_f
			d = d + aim*command_f
		elif "up" in line:
			command_u = int(line.replace("up", ""))
			aim = aim - command_u
		else: #down because input is always well-formatted
			command_d = int(line.replace("down", ""))
			aim = aim + command_d
	print(f"The multiplication result is {f}*{d}={f*d}")
	

main()
