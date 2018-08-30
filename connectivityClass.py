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
		print (dataframeList)

		df = pd.DataFrame(dataframeList, columns = ['Ch_A', 'Ch_B', 'SyncValue'])
		#print(df)
		links = df.loc[(df['SyncValue'] > 0.8) & (df['Ch_A'] != df['Ch_B'])]
		print (links)
		return links


	def GenerateGraphFromPandas(self, links):
		G  = nx.from_pandas_edgelist(links, 'Ch_A','Ch_B')
		#plot the network
		nx.draw(G, with_labels=True, node_color = 'red', node_size = 50, edge_color = 'black', linewidths = 1, font_size = 4,grid = True)
		plt.show()

'''
if __name__ == "__main__":

	#lets createa an istance of MatrixGenerate class
	M = MatrixGenerate()
	
	SynchronyFileLocation = 'isi_distance.npy'
	links = M.generatePandasDF(SynchronyFileLocation)
	M.GenerateGraphFromPandas(links)
'''



