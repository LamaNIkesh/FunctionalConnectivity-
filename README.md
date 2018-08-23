# Synchrony based connectivity estimation attempt

Attempt to create a connectivity map using the synchrony levels measured from the ISI and SPIKE-distance metrics. So, synchrony levels for all one-one connections are stored into a dictionary as a key value pair where key is the channel number and the value is the synchrony level. Then these keys are taken as nodes and values as edges that connects the nodes. 

## SynchonryMeasures 
This folder contains pyspike library to calculate ISI and SPIKE-distance metrics for synchrony levels. Synchrony levels obtained from these are then stored as numpy array and used by connectivityClass.py

## connectivityClass.py
Takes in .npy array and convert into panda dataframe to generate a simple graph with nodes being the recorded channels and undirected edges for now.


 ![sample connectivity](https://github.com/LamaNIkesh/FunctionalConnectivity-/images/Connectivity_500.png)	
