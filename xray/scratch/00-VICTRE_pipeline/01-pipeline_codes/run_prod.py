##### The scripts are used to test each steps in the VITRE pipeline
#### created by Shenghua He
#### date: 9/26/2019

from helper_function import *
import os
import time

## Directory for phantom output
dataset_root_folder = os.path.expanduser('~/00-VICTRE_pipeline/02-phantom_set/')

## configurations for job running
#phantom_type = 'dense'
#fetch_seed = 1700001
phantom_type = 'scattered'
fetch_seed = 935721109
num_GPU = 0

## lesion insertion
#insert_cmd = 'python lesion_insert.py {0:} {1:} {2:}'.format(fetch_seed, phantom_type, dataset_root_folder)
#print(insert_cmd)
#os.system(insert_cmd)

## xray imaging: signal absent (SA)
# xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(fetch_seed, phantom_type, dataset_root_folder, num_GPU, 10.06, 0, 0)
# print(xray_cmd)
# os.system(xray_cmd)

## mammo ROI extraction: SA
#mammoROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'mammo', 'SA')
#print(mammoROI_cmd)
#os.system(mammoROI_cmd)

## xray imaging: signal present (SP)
## parameters: random seed, phantom type, output dataset root folder, GPU number, lesion density (for testing), inserted or not, whether to generate flatfield
#xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:} {6:}'.format(fetch_seed, phantom_type, dataset_root_folder, num_GPU, 10.06, 1, 0)
#print(xray_cmd)
#os.system(xray_cmd)

## mammo ROI extraction: SP
#mammoROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:} {3:} {4:}'.format(fetch_seed, phantom_type, dataset_root_folder, 'mammo', 'SP')
#print(mammoROI_cmd)
#os.system(mammoROI_cmd)

## DBT reconstruction
## parameters: random seed, phantom type, data set root folder, inserted or not
dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, dataset_root_folder, 0)
print(dbt_cmd)
os.system(dbt_cmd)

# dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, dataset_root_folder, 2)
# print(dbt_cmd)
# os.system(dbt_cmd)


