# -*- coding: utf8 -*-
import os
import random
from shutil import copyfile
import re
import subprocess
#import commands
import argparse
import time

### directory configuration for lesion insertion commands
# lesion_cmd_path = os.path.expanduser('/shared/aristotle/Phantom/00-VICTRE_pipeline/00-base_input_files/04-other_shared_files/LesionInsertion')
# lesion_cmd_path = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/04-other_shared_files/LesionInsertion')
lesion_cmd_path = os.path.expanduser('/scratch/00-VICTRE_pipeline/01-pipeline_codes/x-ray_runs/lesion_insert_cmd')

def generate_folder(folder):
        if not os.path.exists(folder):
                os.mkdir(folder)

parser = argparse.ArgumentParser()
parser.add_argument("RndSeed",type=int)			# random seed taken from phantom file name
parser.add_argument("phantom_type",type=str)  		# focal spot locations X,Y,Z (mm)
parser.add_argument("phantom_data_folder", type=str)
parser.add_argument("signal_model_code", type=int)
args = parser.parse_args()


## start time 
start_time = time.time()

phantom_type = args.phantom_type
rand_seed = args.RndSeed

# data_root_folder = os.path.expanduser('~/07-Datasets')
data_root_folder = args.phantom_data_folder
patient_folder = os.path.join(data_root_folder,'{}'.format(rand_seed))
signal_model_code = args.signal_model_code

## parse the mhd file to get the information about the phantom
mhd_file = os.path.join(patient_folder, 'pc_{}_crop.mhd'.format(rand_seed))
elementSpac = 0
dimX, dimY, dimZ = 0 ,0 ,0
offsetX, offsetY, offsetZ = 0, 0, 0
with open(mhd_file, 'r+') as f:
	lines = f.readlines()
	for line in lines:
		splits = re.split(r'[ ,;,\t]', line.rstrip())
		if splits[0] == 'ElementSpacing':
			print(line)
			print(splits)
			elementSpac = splits[-1]
		if splits[0] == 'Offset':
			print(line)
			print(splits)
			offsetX, offsetY, offsetZ = splits[-3], splits[-2], splits[-1]
		if splits[0] == 'DimSize':
			print(line)
			dimX, dimY, dimZ = splits[-3], splits[-2], splits[-1]
			print(splits)

## insert command preparation
#echo $var1
#lesion_cmd_path = os.path.expanduser('~/05-VICTRE/LesionInsertion')
lesinsertCmd='python2 {0:}/lesionInsertion.py {1:} 0 69 630 {2:} {3:} {4:} {5:} 0 0 0 {6:} {7:} {8:} 100 166 115 {9:} {10:}'.format(lesion_cmd_path, rand_seed, elementSpac, offsetX, offsetY, offsetZ, dimX, dimY, dimZ, patient_folder, signal_model_code)
print(lesinsertCmd)
# results = commands.getoutput(lesinsertCmd)
# os.system(lesinsertCmd)
results = subprocess.check_output(lesinsertCmd, shell = True)
# log_folder = os.path.join(patient_folder, 'logs')
log_folder = os.path.join(patient_folder,'logs')
generate_folder(log_folder)
log_file = os.path.join(log_folder, 'log_insert_{}.txt'.format(signal_model_code))
with open(log_file,'w+') as f:
	results = str(results)
	f.write(results)

## duration time of lesion insertion measured in hours
duration_time = (time.time() - start_time)/60/60
time_file = os.path.join(log_folder, 'time_lesion_insert_{}.txt'.format(signal_model_code))
with open(time_file, 'w+') as f:
    f.write('Lesion insertion time cost: {0:.3f} hours\n'.format(duration_time))
