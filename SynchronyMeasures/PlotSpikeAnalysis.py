import matplotlib.pyplot as plt
import numpy as np
import pyspike as spk
import time
from multiprocessing import Process,Pool

#############################################################################
# Some multiprocessing attempts
#the function itself doesnt have any multiprocessing implemented but different arguements will run concurrently 
def multiprocessFunctions(analysis):

	if analysis == 'isi_distance':
		#print ('isi distance')
		print("ISI distance calcualtion started!!!")
		plt.figure()
<<<<<<< HEAD
<<<<<<< HEAD
		isi_distance = spk.isi_distance_matrix(spike_trains, interval = None)
		isi_distance[isi_distance > 1] = 1
		print (isi_distance)
		np.save("isi_distance", isi_distance)
		np.savetxt("isi_distance.csv",isi_distance, delimiter = ",")     
=======
=======
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
		isi_distance = spk.isi_distance_matrix(spike_trains, interval = (0,5000))
		isi_distance[isi_distance > 1] = 1
		print (isi_distance)
		np.save("isi_distance", isi_distance)     
<<<<<<< HEAD
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
=======
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
		plt.imshow(isi_distance,clim=(0.0, 1.0), interpolation='nearest')
		plt.colorbar()
		plt.title("ISI-distance(0-100ms)")
		print ('----------Took %s seconds for isi distance-----'%(time.time() - start_time))
		plt.show()
	elif analysis == 'spike_distance':
		#print ('spike distance')
		plt.figure()
		spike_distance = spk.spike_distance_matrix(spike_trains, interval=(0,100))
		spike_distance[spike_distance > 1] = 1
		np.save("spike_distance", spike_distance)
		plt.imshow(spike_distance, clim=(0.0, 1.0), interpolation='nearest')
		plt.colorbar()
		plt.title("SPIKE-distance(0-100ms)")
		print ('----------Took %s seconds for spike distance-----'%(time.time() - start_time))
		plt.show()
	elif analysis == 'spike_sync':
		#print ('spike sync')
		plt.figure()
		spike_sync = spk.spike_sync_matrix(spike_trains, interval=(3300,3500))
		plt.imshow(spike_sync, interpolation='none')
		plt.colorbar()
		plt.title("SPIKE-Sync")
		print ('----------Took %s seconds for spike_sync-----'%(time.time() - start_time))
		plt.show()
	else:
		pass


if __name__ == '__main__':

	start_time = time.time()
<<<<<<< HEAD
<<<<<<< HEAD
	spike_trains = spk.load_spike_trains_from_txt("final_interpolated.txt", 5000, separator = " ", is_sorted = True, ignore_empty_lines = False)
=======
	spike_trains = spk.load_spike_trains_from_txt("final_interpolated.txt", 5000)
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
=======
	spike_trains = spk.load_spike_trains_from_txt("final_interpolated.txt", 5000)
>>>>>>> 0cedc72f5f2d2fc87dd0013b90157c1498ad2a7e
	#spike_trains = spk.load_spike_trains_from_txt("final_interpolated.txt", edges = (0,5000))
	#spike_trains = spk.load_spike_trains_from_txt("PySpike_testdata.txt", 4000)
	print (len(spike_trains))
	print (spike_trains)
	#spike_trains = spk.load_spike_trains_from_txt("../examples/final.txt", 4000)
	'''
	spiketrain = []
	with open("final_interpolated.txt") as f:
		for line in f:
			spiketrain.append(line)
			#print spiketrain
	'''
	#processors pool
	p = Pool(5)
	#running three different plots in parallel in different processors
	#basically three instances of the function is run in three differnt processors parallely
	#p.map(multiprocessFunctions,['isi_distance', 'spike_distance'])
	p.map(multiprocessFunctions,['isi_distance'])
	#mlp = Process(target = multiprocessFunctions, args = [(spike_trains, 'isi_distance'), (spike_trains, 'spike_distance'),(spike_trains, 'spike_sync')])
	#mlp.start()
	#mlp.join()
	'''
	plt.figure()
	isi_distance = spk.isi_distance_matrix(spike_trains)
	plt.imshow(isi_distance, interpolation='none')
	plt.colorbar()
	plt.title("ISI-distance")
	print ('----------Took %s seconds for isi distance-----'%(time.time() - start_time))

	plt.figure()
	spike_distance = spk.spike_distance_matrix(spike_trains, interval=(0,10000))
	plt.imshow(spike_distance, interpolation='none')
	plt.colorbar()
	plt.title("SPIKE-distance")
	print ('----------Took %s seconds for spike distance-----'%(time.time() - start_time))
	plt.figure()
	spike_sync = spk.spike_sync_matrix(spike_trains, interval=(0,10000))
	plt.imshow(spike_sync, interpolation='none')
	plt.colorbar()
	plt.title("SPIKE-Sync")
	print ('----------Took %s seconds for spike_sync-----'%(time.time() - start_time))

	plt.show()
	'''
    #print ("------It took %s seconds to process and plot-------"%(time.time()-start_time))
