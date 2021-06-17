from helper_function import *
import os
import time
import numpy as np

## Directory for phantom output
dataset_root_folder = os.path.expanduser('~/08-Phantom_Set')  ## phantom output folder
#recompression_file = os.path.expanduser('~/00-VICTRE_pipeline/01-pipeline_codes/re_compression_list.txt')
recompression_file = os.path.expanduser('~/00-VICTRE_pipeline/01-pipeline_codes/recompress_unsuccess_list.txt')
## load the re-compression phantom set
##seed_arr = np.int32(np.loadtxt(recompression_file))

seed_arr = []
with open(recompression_file, 'r+') as f:
    lines = f.readlines()
    for line in lines:
        seed_arr.append(np.int32(line.strip()))

## configurations for job running
phantom_type = 'scattered'

for i in range(len(seed_arr)):
	fetch_seed = seed_arr[i]
	# phantom compression and cropping
	comp_crop_cmd = 'python phantom_compress_crop.py {0:} {1:} {2:}'.format(fetch_seed, phantom_type, dataset_root_folder)
	print(comp_crop_cmd)
	os.system(comp_crop_cmd)
