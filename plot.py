import glob
import matplotlib.pyplot as plt 
import nympy as np 

def analyze (fname):
	#Here 
	#Read Data
		#Use a list
	rawDatalist = np.loadtxt(fname, dtype='i2')
	smoothDataList = smoothdata(data) #this list should return the formula with y and n

	print(smoothDataList)


	#Smooth using the formula
	#find pulse
	pulses=[]
	    #loop (while loop) through some smooth data and find the rise
	    #Have an if statement here, if the third position data[n+2] is greater than the first position
	    #data[n], then add i to pulses

	    	#  
	#compute the pulse
	#plot
	_,axes = plt.subplots(nrows=2)
	axes[0].plot(rawDatalist, linewidth=.2)
	axes[0]set(title='something')

		#show the smooth data graph
	axes[1]

	#calculate the areas and build the result
	


def smoothdata(data):
	#Start with a formula
	smoothList = data.copy()
	for n in range(3, len(data)-3):
		smoothList[n] = (data[n-3] + 2*data[n-2] + 3*data[n-1] + 3*data[n] + 3*data[n+1] + 2*data[n+2] + data[n+3])//15



def main():
	for fname in glob.glob('*.dat'):
		analyze(fname)

