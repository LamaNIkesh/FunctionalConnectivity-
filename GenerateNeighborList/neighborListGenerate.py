#######################################################################
#Small script that allows to generate channel neighbor list of any size
#@author: Nikesh Lama
#Date: September 2018
#######################################################################

import numpy as np
import time
import csv
import os

#print(len(matrix))

def in_bounds(matrix, row, col):
	"""
	Checks if there are any neighbors or not
	"""
	if row < 0 or col < 0:
		return False
	if row > len(matrix)-1 or col > len(matrix)-1:
		return False
	return True


def traversal(matrix, radius, rowNumber, colNumber, traversalDirection = 'up'):
	"""
	Returns: closest neighbors based on the radius provided. The boundry is more like a circle. 
			Note: Up and down traversal is the same distance as radius, but for every left step it also traverses 
				  up and down but one less step than the radius and this decreases with each left or right step resulting in a oval shape.
				  eg : 	       []
				             [][][]
				           [][][][][]
				         [][][] *[][][]
				           [][][][][]
				             [][][]
				               []
	"""
	#Simple up traversal
	if traversalDirection == 'up':
		for row in range(radius):
			if in_bounds(matrix, rowNumber - row - 1, colNumber):
				print(str(matrix[rowNumber-row - 1][colNumber]))
				#neighborList[counter].append(matrix[rowNumber-row - 1][colNumber])
				f.write(matrix[rowNumber-row - 1][colNumber])
				f.write(",")
	#simple down traversal
	elif traversalDirection == 'down':
		for row in range(radius):	
			if in_bounds(matrix, rowNumber + row + 1, colNumber):
				print(str(matrix[rowNumber+row + 1][colNumber]))
				#neighborList[counter].append(matrix[rowNumber+row + 1][colNumber])
				f.write(matrix[rowNumber+row + 1][colNumber])
				f.write(",")
	#right traversal, at each step up and down traversal are done recursively
	elif traversalDirection == 'right':
		for column in range(radius):	
			if in_bounds(matrix, rowNumber, colNumber + column + 1):
				print(str(matrix[rowNumber][colNumber + column + 1]))
				f.write(matrix[rowNumber][colNumber + column + 1])
				f.write(",")
				#neighborList[counter].append(matrix[rowNumber][colNumber + column + 1])
				#at every right traverse, up traverse and down traverse are done
				newCol = colNumber+column+1
				newRadius = radius - column -1 # right and up traverse is one less element
				if newRadius>0:
					#move up 
					traversal(matrix, newRadius, rowNumber, newCol, traversalDirection = 'up')
					#move down
					traversal(matrix, newRadius,rowNumber, newCol, traversalDirection = 'down')	

	#left traversal, at each step up and down traversal are done recursively			
	elif traversalDirection == 'left':
		for column in range(radius):	
			if in_bounds(matrix, rowNumber, colNumber - column - 1): #subtracting 1 because the index starts with 0
				print(str(matrix[rowNumber][colNumber - column - 1]))
				#neighborList[counter].append(matrix[rowNumber][colNumber - column - 1])
				#at every right traverse, up traverse and down traverse are done
				newCol = colNumber-column-1
				newRadius = radius - column -1 # left and up traverse is one less element
				if newRadius>0:
					#move up 
					traversal(matrix, newRadius, rowNumber, newCol, traversalDirection = 'up')
					#move down
					traversal(matrix, newRadius,rowNumber, newCol, traversalDirection = 'down')	


def neighbors(matrix, radius, rowNumber, colNumber):
	
	#Up traverse
	print("up traverse!!")
	traversal(matrix, radius, rowNumber, colNumber, traversalDirection = 'up')
	
	#Down traverse
	print("down traverse!!")
	traversal(matrix, radius, rowNumber, colNumber, traversalDirection = 'down')
	
	#Left traverse
	print("left traverse!!")
	traversal(matrix, radius, rowNumber, colNumber, traversalDirection = 'right')
	#Right traverse
	print("right traverse!!")
	traversal(matrix, radius, rowNumber, colNumber, traversalDirection = 'left')



channel_list = []
#lets import csv file with list of biocam probe channel numbers in 2D grid

with open ("ProbeLayoutBioCam.csv") as f:
	reader = csv.reader(f)
	for row in reader:
		channel_list.append(row) 

#print(channel_list)

channel_list = np.array(channel_list)
print((channel_list))
print(len(channel_list))
print(len(channel_list[0]))


neighborList = [[]]
#print (channel_list)
rows = 64
columns = 64
if os.path.exists('NeighborListNew'):
	os.remove('NeighborListNew')

f = open("NeighborListNew_5.csv", "w+")

for i in range(columns):
	for j in range(rows):
		neighbors(channel_list, 5, i, j)
		f.write("\n")
		#neighborList[0].append(neighborHolder)

f.close()
# #Finding neighbors for all the channels and writing the neighbors as a csv file indexed with the channel numbers
# with open ('neighborList.csv','w') as writeFile:
# 	#lets iterate through each 
# 	writer = csv.writer(writeFile)
# 	writer.writerows(writeFile)
# writeFile.close()
