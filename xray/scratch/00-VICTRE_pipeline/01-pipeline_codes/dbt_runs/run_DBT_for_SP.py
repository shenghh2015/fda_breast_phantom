##### The scripts aredbtROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'dbt', 'SA')
#used to test each steps in the VITRE pipeline
#### created by Shenghua He
#### date: 9/26/2019, modified date: 10/24/2019

# from helper_function import *
# from sync_check import *
import os
import time
import random
import glob
import numpy as np
import argparse
from consistency_dbt import *


## Directory for phantom output
#phantom_set_folder = os.path.expanduser('~/08-Phantom_Set')
#xray_set_folder = os.path.expanduser('~/09-xray_images/')
xray_set_folder = os.path.expanduser('/scratch/xray_set/03-xray_set')
dbt_set_folder = xray_set_folder

signal_model_code = 1  ## a code that specify the signal model used in this study

# generate_folder(dbt_set_folder)

## sleep for a random number of seconds
sleep_time_range = 10
sleep_time = random.randint(0,sleep_time_range)
time.sleep(sleep_time)
## get the patient list in the phantom set folder
folder_list = glob.glob(os.path.join(xray_set_folder,'*'))
phantom_list = []
for folder in folder_list:
	if os.path.isdir(folder):
		phantom_list.append(np.int32(os.path.basename(folder)))

# xray_folder_list = glob.glob(os.path.join(xray_set_folder,'*'))
# xray_patient_list = []
# for folder in xray_folder_list:
#         if os.path.isdir(folder):
#                 xray_patient_list.append(np.int32(os.path.basename(folder)))

## remove the touched patient folders
# for folder in xray_patient_list:
#     if folder in patient_list:
#         patient_list.remove(folder)

fetch_seed = 0
for fetch_ in phantom_list:
	CONSIS_FLAG = consistency_dbt_check(xray_set_folder = xray_set_folder, random_seed = fetch_, insert_label = 'l')
	## configurations for job running
	# ready_status, phantom_folder = xray_sync_check(phantom_set_folder=phantom_set_folder, output_set_folder=xray_set_folder,random_seed = fetch_, insert_label = 'nl', signal_model_code = 0)
	if CONSIS_FLAG:
		fetch_seed = fetch_
		print('Take data from phantom: {}'.format(fetch_))
		break

if not fetch_ == 0:
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
	print('Phantom type: '+phantom_type)
	## place an taken flag to accupy the data
	status_folder = os.path.join(xray_set_folder,'{}'.format(fetch_seed),'status_flags')
	if not os.path.join(status_folder):
		os.mkdir(status_folder)
	with open(os.path.join(status_folder, 'dbt_insert.txt'),'w+') as f:
		f.write('Yes\n')
	## FBP reconstruction
	dbt_cmd = 'python2 DBTrecon.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, dbt_set_folder, 1)
	print(dbt_cmd)
	os.system(dbt_cmd)
	## DBT ROV extraction
	dbtROI_cmd = 'python2 ROI_extraction.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(fetch_seed, phantom_type, dbt_set_folder, 'dbt', 'SP', 1)
	print(dbtROI_cmd)
	os.system(dbtROI_cmd)
