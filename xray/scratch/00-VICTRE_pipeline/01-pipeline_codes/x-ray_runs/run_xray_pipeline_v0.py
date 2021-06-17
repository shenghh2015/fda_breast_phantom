##### The scripts aredbtROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'dbt', 'SA')
#used to test each steps in the VITRE pipeline
#### created by Shenghua He
#### date: 9/26/2019, modified date: 10/24/2019

from helper_function import *
from sync_check import *
import os
import time
import random
import glob
import numpy as np
import argparse


## Directory for phantom output
#phantom_set_folder = os.path.expanduser('~/08-Phantom_Set')
#xray_set_folder = os.path.expanduser('~/09-xray_images/')
phantom_set_folder = os.path.expanduser('~/12-data_from_other_folders/01-Condor/02-phantom_set')
xray_set_folder = os.path.expanduser('~/12-data_from_other_folders/01-Condor/03-xray_images')

signal_model_code = 1  ## a code that specify the signal model used in this study

parser = argparse.ArgumentParser()
parser.add_argument("gpu_num",type=int)		
args = parser.parse_args()

generate_folder(xray_set_folder)

## sleep for a random number of seconds
sleep_time_range = 10
sleep_time = random.randint(0,sleep_time_range)
time.sleep(sleep_time)
## get the patient list in the phantom set folder
folder_list = glob.glob(os.path.join(phantom_set_folder,'*'))
patient_list = []
for folder in folder_list:
	if os.path.isdir(folder):
		patient_list.append(np.int32(os.path.basename(folder)))

fetch_seed = 121760580

for fetch_ in patient_list:
	## configurations for job running
	ready_status, phantom_folder = xray_sync_check(phantom_set_folder=phantom_set_folder, output_set_folder=xray_set_folder,random_seed = fetch_, insert_label = 'nl', signal_model_code = 0)
	print(ready_status)
	if not ready_status:
		continue
	else:
		fetch_seed = fetch_
		break

## phantom type
phantom_type_digit = fetch_seed%100000000//10000000
phantom_type = 0
if phantom_type_digit == 1:
	phantom_type = 'dense'
elif phantom_type_digit == 2:
	phantom_type = 'hetero'
elif phantom_type_digit == 3:
	phantom_type = 'scattered'
elif phantom_type_digit == 4:
	phantom_type = 'fatty'

print(phantom_type)
## x-ray imaging 
# num_GPU = 3
num_GPU = args.gpu_num
signal_model_code = 1
isInserted, isField, zero_signal_model_code = 0, 0, 0
xray_cmd = 'python2 MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(fetch_seed, phantom_type, xray_set_folder, num_GPU, isInserted, isField, zero_signal_model_code)
print(xray_cmd)
os.system(xray_cmd)
gen_success = xray_generation_check(output_set_folder=xray_set_folder, random_seed = fetch_seed, insert_label = 'nl', signal_model_code = zero_signal_model_code)

## lesion insertion and x-imaging for that
ready_status, phantom_folder = xray_sync_check(phantom_set_folder=phantom_set_folder, output_set_folder=xray_set_folder,random_seed = fetch_seed, insert_label = 'l', signal_model_code = signal_model_code)
if gen_success and ready_status:
	insert_cmd = 'python2 lesion_insert.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, xray_set_folder, signal_model_code)
	print(insert_cmd)
	os.system(insert_cmd)
	isInserted, isField = 1, 0
	xray_cmd = 'python2 MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(fetch_seed, phantom_type, xray_set_folder, num_GPU, isInserted, isField, signal_model_code)
	print(xray_cmd)
	os.system(xray_cmd)
	gen_success = xray_generation_check(output_set_folder=xray_set_folder, random_seed = fetch_seed, insert_label = 'l', signal_model_code = signal_model_code)

	## mammo ROI extraction: SA
	mammoROI_cmd = 'python2 ROI_extraction.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(fetch_seed, phantom_type, xray_set_folder, 'mammo', 'SA', zero_signal_model_code)
	print(mammoROI_cmd)
	os.system(mammoROI_cmd)

	## mammo ROI extraction: SP
	mammoROI_cmd = 'python2 ROI_extraction.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(fetch_seed, phantom_type, xray_set_folder, 'mammo', 'SP', signal_model_code)
	print(mammoROI_cmd)
	os.system(mammoROI_cmd)
