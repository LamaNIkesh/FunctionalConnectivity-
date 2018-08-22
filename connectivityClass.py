##############################################################
#				Class for connectivity estimation			 #
#					Nikesh Lama  August 2018				 #
##############################################################
import warnings
#lots of warning due to version mismatch for numpy,sklearn etc..
warnings.filterwarnings("ignore")

import numpy as np 
import matplotlib.pyplot as plt 
import time
from multiprocessing import Process,Pool
import pandas as pd
import readSpikeTrain
import networkx as nx
from multiprocessing import Process,Pool
import threading

class MatrixGenerate(object):
	""" This class is a simplist approach to use the synchrony information obtained from ISI and SPIKE-distance metrics
	to generate adjaceny matrix where nodes are the channels and the edges are the synchrony levels. 

	Usage:

	"""

	def __init__(self):
		pass

	def generatePandasDF(self,adjacencyMatrix = ''):
		AdjacencyArray = np.load(adjacencyMatrix)
		print(AdjacencyArray.shape[0])
		#rows/columns size -- since we are dealing with a square matrix one info is enough
		rows_columns = AdjacencyArray.shape[0]

		df = pd.DataFrame(AdjacencyArray, index = AdjacencyArray[:,0])
		print(df)
		links = df.reset_index()
		links.columns = ['var1','var2','value']
		links
		return df,links


	def GenerateGraphFromPandas(self, links):
		G  = nx.from_pandas_edgelist(links, 'Ch_A','Ch_B')
		#plot the network
		nx.draw(G, with_labels=True, node_color = 'lightblue', node_size = 100, edge_color = 'grey', linewidths = 1, font_size = 10)
		plt.show()

#
'''
M = MatrixGenerate()
pd_df,links = M.generatePandasDF('isi_distance.npy')
#print(np.load('isi_distance.npy'))
M.GenerateGraphFromPandas(links)
'''

# def multiprocess(items, start, end):

# 	for item in items[start:end]
# 		try:
# 			api.my_operation(item)
# 		except Exception:
# 				print ('Error with the item')


AdjacencyArray = np.load('isi_distance.npy')
print(AdjacencyArray.shape[0])
#rows/columns size -- since we are dealing with a square matrix one info is enough
rows_count = AdjacencyArray.shape[0]
columns_count = AdjacencyArray.shape[1]
'''
df = pd.DataFrame(AdjacencyArray, index = AdjacencyArray[:,0])
#print(df.count)
links = df.reset_index(drop = True)
links.columns = ['var1','var2','value']
links
'''
#lets rearrange the square matrix into a 3 column matirx where first and second columns
#are channels and third is the synchorny between them. we will put these into a panda dataframe

#df = pd.DataFrame(columns = ['Ch_A', 'Ch_B', 'SyncValue'])

dataframeList = []
print(dataframeList)



for i in range(20): #only using 10 rows for testing
	for j in range(20): #only using 10 columns for testing
		#print('Ch_A: {} -- Ch_B: {} -- SyncValue: {}'.format(i,j,AdjacencyArray[i,j]))
		#df.append({'Ch_A':i, 'Ch_B':j, 'SyncValue': AdjacencyArray[i,j]}, ignore_index = True)
		if AdjacencyArray[i][j] < 0.6 :
			AdjacencyArray[i][j] = 0
		elif AdjacencyArray[i][j] > 0.8:
			AdjacencyArray[i][j] = 0.8
		else:
			pass
		if AdjacencyArray[i][j]>0:	
			data_input = [i,j,AdjacencyArray[i][j]]
			dataframeList.append(data_input)
		#dataframeList[i].append(j)
		#dataframeList[i].append(AdjacencyArray[i,j])
		pass

	print('Row {} done processing!!'.format(i))        
print (dataframeList)

df = pd.DataFrame(dataframeList, columns = ['Ch_A', 'Ch_B', 'SyncValue'])
print(df)

M = MatrixGenerate()
M.GenerateGraphFromPandas(df)