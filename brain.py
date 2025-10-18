import random as rng
from matplotlib import pyplot as plt
import numpy as np
import math

def roll_dice(n):
	possible_results = range(1,7)
	removed_number = 0
	if n <= 0:
		dice_results = [rng.choice(possible_results), rng.choice(possible_results)]
		dice_results.sort()
		removed_number = dice_results.pop(1)
	else:
		dice_results = [rng.choice(possible_results) for _ in range(n)]

	
	dice_results.sort(reverse=True)
	if n >= 2 and dice_results[1] == 6:
			final_result = "Critical"
	elif dice_results[0] == 6:
		final_result = "Success"
	elif dice_results[0] in [4, 5]:
		final_result = "Partial"
	else:
		final_result = "Fail"

	if removed_number:
		dice_results.append(removed_number)
	return(final_result, dice_results)


def circ_sectors(segments, fill=0):
	fig = plt.figure(figsize=(2,2))
	line_colour = "#dddddd"
	background_colour = "#1a191e"
	plt.rcParams['axes.facecolor'] = background_colour
	fig.patch.set_facecolor(background_colour)
	plt.axis('off')  
	linewidth = 3.0
	plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
	plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
	angle = np.linspace(0, 2*math.pi, 100)
	x_circle = [math.cos(x) for x in angle]
	y_circle = [math.sin(x) for x in angle]

	for i in range ( segments ):
		theta = (i * (2*math.pi) / segments) + math.pi/2
		plt.plot([0, (math.cos(theta))], [0, (math.sin(theta))], line_colour, linewidth=linewidth)
	for i in range(fill):
		min_angle = (-i * (2*math.pi) / segments) + math.pi/2
		max_angle = ((-i-1) * (2*math.pi) / segments) + math.pi/2
		xs = [0.0, math.cos(min_angle)]
		ys = [0.0, math.sin(min_angle)] 
		seg_angle = np.linspace(min_angle, max_angle, 100)
		for theta in seg_angle:
			xs.append(math.cos(theta))
			ys.append(math.sin(theta))
		xs.append(math.cos(max_angle))  
		ys.append(math.sin(max_angle))
		plt.fill(xs, ys, "r")

	plt.axis('equal')
	plt.plot(x_circle,y_circle, line_colour, linewidth=linewidth*2)
	return(fig)
