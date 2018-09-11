
import warnings
#few warnings due to version mismatch for numpy,sklearn etc..
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pyspike as spk
import time
import csv
import pandas as pd
#import networkx as nx

from multiprocessing import Pool

if __name__ == '__main__':

	'''
	We want to perform isi_distance synchrony measures between all two spike trains
	from a list of 4096 spike trains. Spatially, if the spike trains are far apart then it is less
	likely there is any effective connections. Hence, to limit the number of synchrony connections
	we want to limit the the bi-variate analysis only to neighboring electrodes from each electrode. 
	
	The electrodes are laid out in a 64x64 grid with co-ordinates as (0,0),(0,1), (0,2).....(0,63)
									 (1,0),(1,1),(1,2)......(1,63)
									 ............................
	The co-ordinates to number mapping is as 			 0,1,2,3,............63,
									 64,65...............127

	Please see the excel sheet in the folder to get better sense of how the neighbors are selected. 	 														
	
	'''

	start_time = time.time()
	spike_trains = spk.load_spike_trains_from_txt("final_interpolated.txt", 5000, 
							separator = " ", is_sorted = True, 
							ignore_empty_lines = False)
	#spike_trains = spk.load_spike_trains_from_txt("final_interpolated.txt", edges = (0,5000))
	#spike_trains = spk.load_spike_trains_from_txt("PySpike_testdata.txt", 4000)
	
	#print (spike_trains)
	
	#lets load neighbor matrix and for each channel, we will only perform bi-variate isi_distance to the neighboring channels
	neighbor_biocam_location = "NeighborListNew_5.csv"
	row_counter = 0
	with open(neighbor_biocam_location,"r") as f:
	    reader = csv.reader(f,delimiter = ",")
	    data = list(reader)
	    #print(row_counter)
	    row_counter = row_counter + 1

	#wrapper function for multiprocessing
	def multi_process_wrapper(args):
		return synchronyCalculation(*args)


	#with open(neighbor_biocam_location) as csvfile:
	#neighbor_electrode_matrix = np.genfromtxt(neighbor_biocam_location, delimiter = ",")

	#print(neighbor_electrode_matrix)
	def synchronyCalculation(t0, t1): #counter is to name the file for easy processing later		
		one_to_one_synchrony = pd.DataFrame(columns = ['Ch_A', 'Ch_B', 'SyncVal'])
		#print(one_to_one_synchrony) 
		dataframelist = [[]]
		#looking at first 20 spike trains
		for i in range(4096):
			data[i] = data[i][:-1]
			#print (data[i])
			NumberOfNeighbors = len(data[i])
			#print(NumberOfNeighbors)

			for j in range(NumberOfNeighbors):
				
				#print(data[i][j])
				#print ("source channel: {}, Neighbor channels: {}".format(i,data[i][j]))

				

				SyncVal = spk.spike_distance(spike_trains[i],spike_trains[int(data[i][j])], interval = (t0,t1))
				#print(SyncVal)
				data_input = [i, int(data[i][j]), SyncVal] 
				dataframelist.append(data_input)
				#one_to_one_synchrony.append({'Ch_A':i, 'Ch_B':data[i][j], 'SyncVal':SyncVal}, ignore_index = True)

		del dataframelist[0]
		df= pd.DataFrame(dataframelist, columns = ['Ch_A', 'Ch_B', 'SyncVal'])
		df = df.loc[(df['SyncVal'] >0.2) & (df['SyncVal'] < 1)]

		#print(df)
		df.to_csv('SynchronyDataframes/{}.csv'.format(t0))

	'''	
	#########################################################################################################################
	##################	MULTI PROCESSING 
	#So the idea is to create synchrony dataframe at every 20 ms and save as csv. 
	#This will be then used to generate a connectivity graph at every 20 ms which can be put togethere as a movie
	timesteps = np.arange(0,2000,20)
	#print(timesteps)
	#print(len(timesteps))
	list_of_arguements = []
	for i in range(len(timesteps)):
		print(i)
		if i < len(timesteps) - 1:
			list_of_arguements.append((timesteps[i], timesteps[i+1]))
		#synchronyCalculation(spike_trains, timesteps[i],timesteps[i+1])
		#print("Finished writing into csv!! {} out of {}".format(i,len(timesteps)))
	#print(list_of_arguements)
	#Now we have a list of arguements that can be fed into the function in parallel utilizing parallel processing/multi processing.

	print(list_of_arguements)

	# with Pool(5) as p:
 #        p.map(synchronyCalculation, [1, 2, 3]))
	p = Pool(16)
	#with Pool(10) as p: # My pc has 16 cores
	p.map(multi_process_wrapper,list_of_arguements)

	########################################################################################

	'''

	########################################################################################
	###	running synchrony data frame calculation individually i.e. one time interval at a time

	synchronyCalculation(400, 600)