"""
Project 6
Author: Jade Barben
Date: 11/22/21
Purpose: To parse through the values, smooth out data and graph out the data points with numpy in order to 
detect potential items that need to be confiscated at airport security. 
'I declare that the following source code was written solely by me. I understand that copying any
source code, in whole or in part, constitutes cheating, and that I will receive a zero on this
project if I am found in violation of this policy.'
"""


#imports of libraries
import glob
import numpy as np
import matplotlib.pyplot as plt

VT = 100
WIDTH = 50

#Converting data into smooth array using formula
def smoothdata(data):
	"""smooths the data using formula"""
	smooth_list = data.copy()
  
	for n in range(3, len(data) -3):
		smooth_list[n] = (data[n - 3] + 2 * data[n -2] + 3 * data[n -1] + 3 * data[n] + 3 * data[n + 1] + 2 * data[n + 2] + data[n +3]) //15
  
	return smooth_list

# analyze the data
def analyze(filename):
	"""analyzes the data and plots points"""
	raw_data = np.loadtxt(filename)
  
	smooth_data = smoothdata(raw_data)
  	
	#find and compute pulse
	pulses = []
	x = 0
  
	while x < len(smooth_data) - 2:
		if smooth_data[x + 2] - smooth_data[x] > VT:
			pulses.append(x)
  
			x += 1
			while x < len(smooth_data) - 2 and smooth_data[x + 1] > smooth_data[x]:
				x += 1
		x += 1
	if not pulses:
		return
  	
  	#plot
	output_str = f'{filename}:\n'
	for x in range(len(pulses)):
		startPos = pulses[x]
		r_width = WIDTH
  
		if x < len(pulses) - 1 and pulses[x] + r_width > pulses[x + 1]:
			r_width = pulses[x + 1] - startPos
		r_width = min(r_width, len(smooth_data) - startPos)
		area = int(sum(raw_data[startPos:startPos + r_width]))
		output_str += f'Pulse {x + 1}: {startPos + 1} ({area})\n'
  
# open the out file
	with open(filename[:-3] + "out", "w") as outfile:
		print(output_str, file=outfile, end="")
  

# Plot the data
	_, axes = plt.subplots(nrows=2)
	axes[0].plot(raw_data, linewidth=.2)
	axes[0].set(title=filename, ylabel="raw")
	axes[1].plot(smooth_data, linewidth=.3)
	axes[1].set(ylabel="smooth")
	#plt.show()
	plt.savefig(filename[:-3] + "pdf")
  

def main():
	for fname in glob.glob("*.dat"):
		analyze(fname)
  
if __name__ == "__main__":
	main()