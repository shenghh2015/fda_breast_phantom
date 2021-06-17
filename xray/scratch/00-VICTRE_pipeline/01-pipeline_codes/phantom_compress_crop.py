#import estCrop_cmd_folders
import os
import random
from shutil import copyfile
import argparse
import subprocess
import time
import sys

def generate_folder(folder):
	if not os.path.exists(folder):
		os.mkdir(folder)

################## command configuration #################
breastCompress_cmd_folder = os.path.expanduser('/scratch/02-breastCompress') # directory to the phantom compression command
breastCrop_cmd_folder = os.path.expanduser('/scratch/03-breastCrop') # directory to the phantom cropping command
febio_folder = os.path.expanduser('/scratch/FEBio-2.9.1')  # FEBio-2.9.1 folder

# Parsing input arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument("RndSeed",type=int)			# random seed taken from phantom file name
parser.add_argument("phantom_type",type=str)  		# focal spot locations X,Y,Z (mm)
parser.add_argument("phantom_data_folder", type=str)
args = parser.parse_args()

################# parameters #########################
phantom_type = args.phantom_type
rand_seed = args.RndSeed
data_root_folder = args.phantom_data_folder
patient_folder = os.path.join(data_root_folder,'{}'.format(rand_seed))

################# phantom compression #################
start_time = time.time()   # start timestamp
# compression configuration 
if phantom_type == 'dense':
	thickness = 40
elif phantom_type == 'hetero':
	thickness = 45
elif phantom_type == 'scattered':
	thickness = 55
elif phantom_type == 'fatty':
	thickness = 60
# compression process
myCmd = '{0:}/breastCompress -s {1:} -t {2:} -a 0 -d {3:} -f {4:}'.format(breastCompress_cmd_folder, rand_seed, thickness, patient_folder, febio_folder)
print(myCmd)
# os.system(myCmd)
# compress log save
log_folder = os.path.join(patient_folder,'logs')
generate_folder(log_folder)
results = subprocess.check_output(myCmd, shell=True)
print(results)
#print(type(results))
print(sys.version)
log_file = os.path.join(log_folder,'log_compression.txt')
with open(log_file,'w+') as f:
	results = str(results)
	f.write(results)
duration_time = (time.time() - start_time)/60/60
with open(os.path.join(log_folder, 'time_compression.txt'),'w+') as f:
	f.write('Phantom compression time: {0:.3f} hours\n'.format(duration_time))

################# phantom cropping #################
start_time = time.time()   # start timestamp
# cropping configuration
x, y, z = 0,0,0
if phantom_type == 'dense':
	x, y, z = 810, 1920, 745
elif phantom_type == 'hetero':
	x, y, z = 1280, 1950, 940
elif phantom_type == 'scattered':
	x, y, z = 1740, 2415, 1140
elif phantom_type == 'fatty':
	x, y, z = 2250, 2760, 1240
# cropping process
myCmd = '{0:}/breastCrop -s {1:} -g 1.0 -x {2:} -y {3:} -z {4:} -d {5:}'.format(breastCrop_cmd_folder, rand_seed, x, y, z, patient_folder)
print(myCmd)
# os.system(myCmd)
# cropping log save
log_folder = os.path.join(patient_folder,'logs')
generate_folder(log_folder)
results = subprocess.check_output(myCmd, shell=True)
log_file = os.path.join(log_folder,'log_cropping.txt')
with open(log_file,'w+') as f:
	results = str(results)
	f.write(results)
duration_time = (time.time() - start_time)/60/60
with open(os.path.join(log_folder, 'time_cropping.txt'),'w+') as f:
	f.write('Phantom cropping time: {0:.3f} hours\n'.format(duration_time))
