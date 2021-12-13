from functions import *



def main(): # Submarine diagnostic
	data = read_file( "03.in" )
	matrix_t = transpose( transform(lambda x: transform(lambda y: int(y), x), transform( list, transform(lambda x: x.replace("\n", ""), data ) ) ) )

	sums = sum_matrix_col_all( matrix_t )
	n = len(matrix_t[0])
	majority = transform(lambda x: 1 if x>n/2 else 0, sums)
	minority = transform( lambda x: 1 if x==0 else 0, majority)
	gamma	= list_bits_to_int( majority ) 
	epsilon = list_bits_to_int( minority ) 
	print(f"Power consumption = {gamma}*{epsilon}={gamma*epsilon}")

	most_matrix  = matrix_t.copy()
	least_matrix = matrix_t.copy()
	oxy = []
	co2 = []
	for i in range(len(matrix_t)):
		# find most&least common bits
		oxy.append( 1 if sum_matrix_col(most_matrix, i)>=(len(most_matrix[0])/2) else 0 )
		if len(most_matrix[0]) == 1:
			oxy = transpose(most_matrix)[0]
			break
		# keep only lines starting with most&least common bits
		most_matrix = transpose( list(filter(lambda x: x[i]==oxy[i], transpose(most_matrix) ) ) )
	for i in range(len(matrix_t)):
		# find most&least common bits
		co2.append( 0 if sum_matrix_col(least_matrix, i)>=(len(least_matrix[0])/2) else 1 )
		if len(least_matrix[0]) == 1:
			co2 = transpose(least_matrix)[0]
			break
		# keep only lines starting with most&least common bits
		least_matrix = transpose( list(filter(lambda x: x[i]==co2[i], transpose(least_matrix) ) ) )

	oxy = list_bits_to_int( oxy )
	co2 = list_bits_to_int( co2 )
	print(f"Life support rating = {oxy}*{co2}={oxy*co2}")
	

main()
