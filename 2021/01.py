from functions import *



def main(): # Sonar sweep
	 data = transform( lambda x: int(x), read_file( "01.in" ) )
	 print(f"There are {get_number_increases(data)} measurements larger than the previous ones.")

	 groups_three = []
	 for i in range( len(data)-2 ):
		  groups_three.append( data[i]+data[i+1]+data[i+2] )
	 print(f"There are {get_number_increases(groups_three)} groups of measurements larger than the previous ones.")	

main()
