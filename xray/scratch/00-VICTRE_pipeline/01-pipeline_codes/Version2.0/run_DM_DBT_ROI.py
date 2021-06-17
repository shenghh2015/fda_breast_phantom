#used to test each steps in the VITRE pipeline
#### created by Shenghua He
#### date: 9/26/2019

from helper_function import *
import os
import time
import glob
import numpy as np
## Directory for phantom output
# dataset_root_folder = os.path.expanduser('~/00-VICTRE_pipeline/02-phantom_set/')
dataset_root_folder = os.path.expanduser('~/00-VICTRE_pipeline/05-cropped_set/')
folder_list = glob.glob(os.path.join(dataset_root_folder,'*'))
patient_list = []
for folder in folder_list:
	if os.path.isdir(folder):
		patient_list.append(np.int32(os.path.basename(folder)))
                # check if the patient data is complete
                #crop_files = glob.glob(os.path.join(folder, 'pc_*_crop.raw.gz'))
                # check if the patient data is being processed

for fetch_seed in patient_list:
	phantom_type_digit = fetch_seed%100000000//10000000
	if phantom_type_digit == 1:
		phantom_type = 'dense'
	elif phantom_type_digit == 2:
		phantom_type = 'hetero'
	elif phantom_type_digit == 3:
		phantom_type = 'scattered'
	elif phantom_type_digit == 4:
		phantom_type = 'fatty'
	
	print(phantom_type)
	## configurations for job running
	num_GPU = 1
        signal_model_case = 3  ## 0: [00001111]; 1:[11110000]; 2:[00000000]; 3:[11111111]
	## lesion insertion
        insert_cmd = 'python lesion_insert.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, dataset_root_folder, signal_model_case)
	print(insert_cmd)
	os.system(insert_cmd)

	## xray imaging: signal absent (SA)
	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(fetch_seed, phantom_type, dataset_root_folder, num_GPU, 10.06, 0, 0)
	print(xray_cmd)
	os.system(xray_cmd)

	## mammo ROI extraction: SA
	mammoROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'mammo', 'SA')
	print(mammoROI_cmd)
	os.system(mammoROI_cmd)

	## xray imaging: signal present (SP)
	## parameters: random seed, phantom type, output dataset root folder, GPU number, lesion density (for testing), inserted or not, whether to generate flatfield
	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(fetch_seed, phantom_type, dataset_root_folder, num_GPU, 10.06, 1, 0)
	print(xray_cmd)
	os.system(xray_cmd)

	## mammo ROI extraction: SP
	mammoROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'mammo', 'SP')
	print(mammoROI_cmd)
	os.system(mammoROI_cmd)

	## DBT reconstruction
	## parameters: random seed, phantom type, data set root folder, inserted or not
	dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, dataset_root_folder, 0)
	print(dbt_cmd)
	os.system(dbt_cmd)

	## DBT ROI extraction: SA
	dbtROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'dbt', 'SA')
	print(dbtROI_cmd)
	os.system(dbtROI_cmd)

	dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, dataset_root_folder, 1)
	print(dbt_cmd)
	os.system(dbt_cmd)

	dbtROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'dbt', 'SP')
	print(dbtROI_cmd)
	os.system(dbtROI_cmd)
	

