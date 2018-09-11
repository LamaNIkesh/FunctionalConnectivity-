'''
author: Nikesh Lama

Naive approach to determine spike trian synchrony of spike trains from 3Brain MEA

This script mainly reads in spike trains after spike detection using Martino Sorbaro et al's algorithms

'''
import time
import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd
import os
from multiprocessing import Process


def readSpikeTrain(filename,channelArray,timestampArray,amplitudeArray):
    """Reads spike train text file

    Keyword arguments:
    filename -- spike train file name
    channelArray -- array that holds the channel number
    timestampArray -- array that holds timestamps
    amplitudeArray -- array that holds amplitude

    """

    spiketrainFile = open(filename,"r")
    #print spiketrainFile.read()
    with open(spiketrainText) as data:
        for line in data:
            counter = 0
            for word in line.split():
                #print word
                #appends elements from each row separated by space into corresponding list
                if counter ==0:
                    channelArray.append(int(word))
                elif counter == 1:
		    #timestamps are actually frame number
		    #to get appropriate time, all timestamps are divided by sampling rate i.e.7702 Hz, to get millisecond we divide by 1000. 
                    timestampArray.append(int(float(word)/7.702))
                elif counter == 2:
                    amplitudeArray.append(int(word))
                else:
                    pass
                counter = counter + 1

def extract_channel(inputmatrix):
    '''
    Extracts each channel with timestamps from provided sorted matrix
    output -- One matrix with each channel being a row with timestamps
    '''
    for i in range(4096): #the number is the number of electrodes
        try:
            spiketrain = inputmatrix.query('Electrode == %d'%i)['Timestamp']
            spiketrain = pd.DataFrame(spiketrain)
            spiketrain = spiketrain.sort_values(by = 'Timestamp', ascending = True)
            new = spiketrain.transpose()
            #print new
<<<<<<< HEAD
<<<<<<< HEAD
            new.to_csv('final_interpolated_ret.txt', header = None, index = None, sep=' ', mode = 'a')
=======
            new.to_csv('final_interpolated.txt', header = None, index = None, sep=' ', mode = 'a')
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
=======
            new.to_csv('final_interpolated.txt', header = None, index = None, sep=' ', mode = 'a')
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
            #
        except:
            print ("electrode not found")


if __name__ == '__main__':

<<<<<<< HEAD
<<<<<<< HEAD
    #spiketrainText = "Hippocampal_Spikes.txt"
    spiketrainText = "retina_INT_Spikes.txt"
=======
    spiketrainText = "Hippocampal_Spikes.txt"
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
=======
    spiketrainText = "Hippocampal_Spikes.txt"
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
    #undetemined array size
    channelId=[]
    Tmsp = []
    Amp = []
    start_time = time.time()
    readSpikeTrain(spiketrainText, channelId, Tmsp, Amp )
    print (channelId)
    readingTime = time.time()-start_time
    print("----Took %s seconds to read spike trains----"%readingTime)
    channelId =np.transpose( np.array(channelId))
    Tmsp = np.transpose( np.array(Tmsp))
    Amp = np.transpose(np.array(Amp))
    matrix = np.column_stack((channelId, Tmsp, Amp))

    pandaDataFrame = pd.DataFrame(matrix, columns = ['Electrode','Timestamp', 'amplitude'])
    print (pandaDataFrame)
    sortingTime = time.time()
    #sortedmatrix = pd.DataFrame([convert(c) for c in l] for l in pandaDataFrame.values)
    sortedMatrix = pandaDataFrame.sort_values(by = 'Electrode', ascending = True)
    sortingTime = time.time()
    print ("-------Sorting took %s seconds-------"%(time.time()- sortingTime))
    sortedMatrix.to_csv('values_interpolated.txt', header = None, index=None, sep=' ', mode = 'a')
    print (sortedMatrix)
    extract_channel(sortedMatrix)

    '''
    print (sortedMatrix.query('Electrode == 2')['Timestamp'])


    ##  Preliminary tests ###
    spiketrain = sortedMatrix.query('Electrode == 2')['Timestamp']
    spiketrain = pd.DataFrame(spiketrain)
    spiketrain = spiketrain.sort_values(by = 'Timestamp', ascending = True)
    new = spiketrain.transpose()
    print new
    new.to_csv('final.txt', header = None, index = None, sep=' ', mode = 'a')
    #with open('final.txt','w') as f:
    #    f.write(new)
    spiketrain_1 = sortedMatrix.query('Electrode == 3')['Timestamp']
    spiketrain_1 = pd.DataFrame(spiketrain_1)
    spiketrain_1 =spiketrain_1.sort_values(by = 'Timestamp', ascending = True)
    new_1 = spiketrain_1.transpose()
    print new_1
    new_1.to_csv('final.txt', header = None, index = None, sep=' ', mode = 'a')

    spiketrain_2 = sortedMatrix.query('Electrode == 4')['Timestamp']
    spiketrain_2 = pd.DataFrame(spiketrain_2)
    spiketrian_2 =spiketrain_2.sort_values(by = 'Timestamp', ascending = True)
    new_2 = spiketrain_2.transpose()
    print new_2

    new_2.to_csv('final.txt', header = None, index = None, sep=' ', mode = 'a')
    ##---preliminary tests ####
    '''
