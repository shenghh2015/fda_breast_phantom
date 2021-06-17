import os
import time
import random
import glob
import numpy as np
import argparse

def check_data_integrity(folder):
	checked_result = False
	phantom_id = os.path.basename(folder)
	folder_dir = os.path.dirname(folder)
	mhd_file = folder+'/pc_{}_crop.mhd'.format(phantom_id)
	crop_file = folder+'/pc_{}_crop.raw.gz'.format(phantom_id)
	loc_file = folder+'/pc_{}.loc'.format(phantom_id)
	inserted_file = folder+'/phantom_l1/pcl_{}_crop.raw.gz'.format(phantom_id)
	if os.path.exists(loc_file) and os.path.exists(mhd_file) and os.path.exists(crop_file) and os.path.exists(inserted_file):
		checked_result = True
	return checked_result

def generate_folder(folder):
	import os
	if not os.path.exists(folder):
		os.system('mkdir {}'.format(folder))

## inputs
xray_set_folder = os.path.expanduser('/scratch/xray_set/03-xray_set')

parser = argparse.ArgumentParser()
parser.add_argument("gpu_num",type=int)
args = parser.parse_args()

num_GPU = args.gpu_num

inserted_folders = glob.glob(xray_set_folder+'/*')

clean_inserted_phantoms = []
for folder in inserted_folders:
	if check_data_integrity(folder) and not os.path.exists(folder+'/status_flags/x-ray-insert-1'):
		clean_inserted_phantoms.append(os.path.basename(folder))

if len(clean_inserted_phantoms)>1:
	indx = random.randint(0, len(clean_inserted_phantoms))
	selected_inserted_phantom = clean_inserted_phantoms[indx]
	status_folder = os.path.join(xray_set_folder, selected_inserted_phantom, 'status_flags')
	generate_folder(status_folder)
	# place a flag file to occupy the phantom process
	with open(status_folder+'/x-ray-insert-1','w+') as f:
		f.write('processing\n')
	
	# get the phantom type
	phantom_type_digit = np.int32(selected_inserted_phantom)%100000000//10000000
	phantom_type = 0
	if phantom_type_digit == 1:
		phantom_type = 'dense'
	elif phantom_type_digit == 2:
		phantom_type = 'hetero'
	elif phantom_type_digit == 3:
		phantom_type = 'scattered'
	elif phantom_type_digit == 4:
		phantom_type = 'fatty'

	# xray imaging
	signal_model_code, isInserted, isField =1, 1, 0
	xray_cmd = 'python2 MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(selected_inserted_phantom, phantom_type, xray_set_folder, num_GPU, isInserted, isField, signal_model_code)
	print(xray_cmd)
	os.system(xray_cmd)

	## mammo ROI extraction: SP
	mammoROI_cmd = 'python2 ROI_extraction.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(selected_inserted_phantom, phantom_type, xray_set_folder, 'mammo', 'SP', signal_model_code)
	print(mammoROI_cmd)
	os.system(mammoROI_cmd)
