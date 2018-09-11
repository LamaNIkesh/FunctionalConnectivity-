import warnings
#few warnings due to version mismatch for numpy,sklearn etc..
warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
import numpy as np
#import pyspike as spk
import time
import csv
import pandas as pd
from multiprocessing import Pool
import networkx as nx

if __name__ == '__main__':

	def list_allCSV():
		fileNameArray = os.listdir('SynchronyDataframes/')
		print(fileNameArray)
		return fileNameArray

	def plotGraph(csvFile):
		#open dataframe obtained from LocalisedSynchrony.py
		#df = pd.read_csv("synchronyDataframe.csv")
		df = pd.read_csv(csvFile)
		print(df)
		#remove entries where synchrony values are zero
		df = df[df.SyncVal != 0]
		#df = df[df.SyncVal > 0.5]
		print(df)

		#create a list of channel number and its position in a grid
		channel_num = []
		for i in range(4096):
			channel_num.append(i)
		#print(channel_num)
		#list of grid co-ordinates
		coordinates = []
		x = 0
		y = 0
		
		for x in range(64):
			for y in range(64):
				coordinates.append((y,x))

		G = nx.from_pandas_edgelist(df, 'Ch_A', 'Ch_B', 'SyncVal')
		edges,weights = zip(*nx.get_edge_attributes(G,'SyncVal').items())
			
		#pos = {0:(0,0),1:(0,1),2:(0,2),3:(0,4),4:(1,0),5:(1,1),6:(1,2),7:(1,3),8:(2,0),9:(2,1),10:(2,2),11:(2,3),12:(3,0),13:(3,1),14:(3,2),15:(3,3)}
		pos = dict(zip(channel_num,coordinates))
		
		#plot the network
		print ("Weights: {}".format(weights))
		plt.title("Connectivity graph based on synchrony level")
		plt.xlabel("Channel(0-64)")
		plt.ylabel("Channel(0-64)")
		nx.draw(G,pos, with_labels=False, node_color = 'black', node_size = 1, edgelist = edges,  edge_color = weights, 
				linewidths = 2, font_size = 6, grid = True, edge_cmap = plt.cm.jet)
		#nx.draw(G,pos, with_labels=False, node_color = 'blue', node_size = 10, linewidths = 1, font_size = 4,grid = True)
		
		plt.setp(plt.gca(), 'ylim', list(reversed(plt.getp(plt.gca(), 'ylim'))))
		
		
		plt.savefig("connectivity_{}.png".format(csvFile[:-4])) #revoming the last 4 chars i.e. .csv
		plt.grid(True)
		#plt.show()


	FileNameList = list_allCSV()

	p = Pool(16)
	#with Pool(10) as p: # My pc has 16 cores
	p.map(plotGraph,FileNameList)