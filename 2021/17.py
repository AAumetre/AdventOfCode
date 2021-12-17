from functions import *
from numpy import array

def shoot(target: List[int], speed: List[int]) -> Tuple[bool, int]:
	probe = array([0,0])
	t = 0
	hit = False
	max_height = 0
	while probe[0] <= target[0][1] and probe[1] >= target[1][0]:
		# update speed & position
		probe += speed
		if speed[0] < 0:
			speed[0] += 1
		if speed[0] > 0:
			speed[0] -= 1
		speed[1] -= 1
		t += 1
		# measure max height and shortest distance to the target center
		max_height = max(max_height, probe[1])
		# check if hit
		if target[0][0] <= probe[0] <= target[0][1] and target[1][0] <= probe[1] <= target[1][1]:
			hit = True
			break
	return hit, max_height
			


def main():
	data = read_file("17.in")[0].replace("target area: x=","").split(", y=")
	target = [ [int(coord) for coord in xy.split("..")] for xy in data ]

	print( target )
	# determine vx_opt: the minimal value of vx st. the probe falls straight in the target
	vx_opt = 0
	Sx = target[0][0] # Target Start x
	while not ( (vx_opt-1)*vx_opt/2 < Sx < vx_opt*(vx_opt+1)/2 ):
		vx_opt += 1 # to be changed wrt. the general direction of the target
	print(f"vx_opt: {vx_opt}")
	# determine vy_opt: highest value which allows not to miss the target when going down
	vy_opt = -target[1][0]-1
	print(f"vy_opt: {vy_opt}")
	
	print(shoot(target,[vx_opt, vy_opt]))
	
	vx_min = vx_opt
	vx_max = target[0][1]+1
	vy_min = -vy_opt-1
	vy_max = vy_opt+1
	success = 0
	for vx in range(vx_min, vx_max):
		for vy in range(vy_min, vy_max):
			hit, _ = shoot(target,[vx, vy])
			if hit: success +=1
	print(f"There are {success} speeds allowing to reach the target")
	
	
	

main()
