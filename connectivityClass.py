#########################################################################################
#				Class for connectivity estimation			#
#					Nikesh Lama  August 2018			#
#########################################################################################
import warnings
#few warnings due to version mismatch for numpy,sklearn etc..
warnings.filterwarnings("ignore")

import numpy as np 
import matplotlib.pyplot as plt 
import time
from multiprocessing import Process,Pool
import pandas as pd
#import readSpikeTrain
import networkx as nx
from multiprocessing import Process,Pool
import threading
import itertools


#This class will be populated with more methods to perform different types of operation
class MatrixGenerate(object):
	""" This class is a simplist approach to use the synchrony information obtained from ISI and SPIKE-distance metrics
	to generate adjaceny matrix where nodes are the channels and the edges are the synchrony levels. 

	Usage:

	"""

	def __init__(self):
		pass

	def generatePandasDF(self,synchronyFileLocation):
		#Loading array with synchrony levels
		AdjacencyArray = np.load(synchronyFileLocation)
		#AdjacencyArray = np.load('isi_distance.npy')
		#rows/columns size -- since we are dealing with a square matrix one info is enough
		rows_count = AdjacencyArray.shape[0] 
		columns_count = AdjacencyArray.shape[1]

		#lets rearrange the square matrix into a 3 column matirx where first and second columns
		#are channels and third is the synchorny between them. we will put these into a panda dataframe

		#df = pd.DataFrame(columns = ['Ch_A', 'Ch_B', 'SyncValue'])

		#empty list which will be populated
		# basically the data is in a nXn matrix. What I want to get is a lists of list of three elements --> channelA, channelB and correlation between them
		# This results in a 3 column matrix. This will later be converted into panda dataframe to fit into networkx library 
		dataframeList = []
		#print(dataframeList)

		# looping through the numpy array, since the channel number is not explicity given but rather only the pairwise correlation is provided
		# with each iteration, the indexes are taken as channel numbers. 

		##TODO --> Spatial information


		for i in range(1024): #only using 200 rows for testing
			for j in range(1024): #only using 200 columns for testing
				#print('Ch_A: {} -- Ch_B: {} -- SyncValue: {}'.format(i,j,AdjacencyArray[i,j]))
				#df.append({'Ch_A':i, 'Ch_B':j, 'SyncValue': AdjacencyArray[i,j]}, ignore_index = True)
								
				if AdjacencyArray[i][j] < 0.4 :
					AdjacencyArray[i][j] = 0
				elif AdjacencyArray[i][j] == 1:
					AdjacencyArray[i][j] = 1
				else:
					pass
				
				#if AdjacencyArray[i][j]>0:	
				data_input = [i,j,AdjacencyArray[i][j]]
				dataframeList.append(data_input)

		for i in range(200): #only using 200 rows for testing
			for j in range(200): #only using 200 columns for testing
				#print('Ch_A: {} -- Ch_B: {} -- SyncValue: {}'.format(i,j,AdjacencyArray[i,j]))
				#df.append({'Ch_A':i, 'Ch_B':j, 'SyncValue': AdjacencyArray[i,j]}, ignore_index = True)
				'''				
				if AdjacencyArray[i][j] < 0.4 :
					AdjacencyArray[i][j] = 0
				elif AdjacencyArray[i][j] == 1:
					AdjacencyArray[i][j] = 0.8
				else:
					pass
				'''
				if AdjacencyArray[i][j]>0:	
					data_input = [i,j,AdjacencyArray[i][j]]
					dataframeList.append(data_input)

					
				#dataframeList[i].append(j)
				#dataframeList[i].append(AdjacencyArray[i,j])
				
				

			#print('Row {} done processing!!'.format(i))        

		#print (dataframeList)

		df = pd.DataFrame(dataframeList, columns = ['Ch_A', 'Ch_B', 'SyncValue'])
		print(df)
		links = df.loc[(df['SyncValue'] > 0.8) & (df['Ch_A'] != df['Ch_B'])]
		#print (links)
		return links


	def GenerateGraphFromPandas(self, links, channel_coordinates):
		
		G  = nx.from_pandas_edgelist(links, 'Ch_A', 'Ch_B', 'SyncValue')
		edges,weights = zip(*nx.get_edge_attributes(G,'SyncValue').items())
		
		#pos = {0:(0,0),1:(0,1),2:(0,2),3:(0,4),4:(1,0),5:(1,1),6:(1,2),7:(1,3),8:(2,0),9:(2,1),10:(2,2),11:(2,3),12:(3,0),13:(3,1),14:(3,2),15:(3,3)}
		pos = channel_coordinates
		#plot the network
		print ("Weights: {}".format(weights))
		plt.title("Connectivity graph based on synchrony level")
		plt.xlabel("Channel(0-64)")
		plt.ylabel("Channel(0-64)")
		nx.draw(G,pos, with_labels=False, node_color = 'black', node_size = 5, edgelist = edges,  edge_color = weights, linewidths = 1, font_size = 6, grid = True, edge_cmap = plt.cm.jet)
		#nx.draw(G,pos, with_labels=False, node_color = 'blue', node_size = 10, linewidths = 1, font_size = 4,grid = True)
		
		plt.setp(plt.gca(), 'ylim', list(reversed(plt.getp(plt.gca(), 'ylim'))))
		
		
		plt.savefig("connectivity.png")
		plt.grid(True)
		plt.show()
		


if __name__ == "__main__":

	#lets createa an istance of MatrixGenerate class
	'''	
	M = MatrixGenerate()
	SynchronyFileLocation = 'isi_distance.npy'
	links = M.generatePandasDF(SynchronyFileLocation)
	np.savetxt("links.csv",links, delimiter = ",") 
	'''
	#create a list of channel number and its position in a grid
	channel_num = []
	for i in range(1024):
		channel_num.append(i)
	#print(channel_num)
	#list of grid co-ordinates
	coordinates = []
	x = 0
	y = 0
	
	for x in range(32):
		for y in range(32):
			coordinates.append((y,x))
	#print (len(coordinates))
	#now that we have our channel number and coordinates, lets create a dictionary of channel number with its corresponding coordinates
	pos = dict(zip(channel_num,coordinates))
	
	print(pos)
	#M.GenerateGraphFromPandas(links, pos)
	#plt.show()

'''
if __name__ == "__main__":

	#lets createa an istance of MatrixGenerate class
	M = MatrixGenerate()
	
	SynchronyFileLocation = 'isi_distance.npy'
	links = M.generatePandasDF(SynchronyFileLocation)
	M.GenerateGraphFromPandas(links)
'''



