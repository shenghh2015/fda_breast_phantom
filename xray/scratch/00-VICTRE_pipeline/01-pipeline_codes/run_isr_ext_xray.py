from helper_function import *
import os
import time

## Directory for phantom output
dataset_root_folder = os.path.expanduser('~/00-VICTRE_pipeline/02-phantom_set/')

## configurations for job running
# num_phantom = 100
phantom_type = 'scattered'
fetch_seed = 935721109
num_GPU = 0

#insert_cmd = 'python lesion_insert.py {0:} {1:} {2:}'.format(fetch_seed, phantom_type, dataset_root_folder)
#print(insert_cmd)
#os.system(insert_cmd)

xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(fetch_seed, phantom_type, dataset_root_folder, num_GPU, 10.06, 0, 0)
print(xray_cmd)
os.system(xray_cmd)

#mammoROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, 'mammo', dataset_root_folder)
#print(mammoROI_cmd)
#os.system(mammoROI_cmd)
