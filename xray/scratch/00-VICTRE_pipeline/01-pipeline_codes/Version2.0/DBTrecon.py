import os
import random
from shutil import copyfile
import subprocess
import argparse
import re
import time
import glob
############### configurations for the DBT reconstruction  ################
flatfield_projection_root_folder = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/03-DBTrecon_files/flatfield')
FBP_cmd_folder = os.path.expanduser('~/05-VICTRE/FBP_DBT_reconstruction_in_C')
concatenate_cmd_folder = os.path.expanduser('~/04-VICTRE_MCGPU')

def generate_folder(folder):
    if not os.path.exists(folder):
	os.mkdir(folder)

# Parsing input arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument("RndSeed",type=int)		    
parser.add_argument("phantom_type",type=str)  	    
parser.add_argument('phantom_data_folder', type = str)
parser.add_argument('inserted', type = int)
args = parser.parse_args()

rand_seed = args.RndSeed
phantom_type = args.phantom_type
isInserted = bool(args.inserted)

## starting time
start_time = time.time()

print(isInserted)

#data_root_folder = os.path.expanduser('~/07-Datasets')
data_root_folder = args.phantom_data_folder
patient_folder = os.path.join(data_root_folder,'{}'.format(rand_seed))
output_data_folder = os.path.join(patient_folder,'dbt_recon')
generate_folder(output_data_folder)

###### FBP reconstruction process ##################

## Concatenation of the DBT projections for preparing the input of the FBP reconstruction
if not isInserted:
    mcgpu_files = 'pc_{}_crop.raw.gz'.format(rand_seed)
else:
    mcgpu_files = 'pcl_{}_crop.raw.gz'.format(rand_seed)

mcgpu_data_folder = os.path.join(patient_folder,'mc_gpu', mcgpu_files)
#concatenate_cmd_folder = os.path.expanduser('~/04-VICTRE_MCGPU')
concateCmd = '{0:}/extract_projection_RAW 3000 1500 25 1 {1:}'.format(concatenate_cmd_folder,mcgpu_data_folder)
os.system(concateCmd)
results = subprocess.check_output(concateCmd, shell=True)
copyfile(os.path.join(patient_folder,'mc_gpu','{}_3000x1500pixels_25proj.raw'.format(mcgpu_files)),os.path.join(output_data_folder,'DBT_{}_25proj.raw'.format(rand_seed))) ## copy the concatenated file to the output folder, so that the reconstruction codes can run


## Preparing flatfield input data for the reconstruction
if not os.path.exists(os.path.join(output_data_folder,'flatfield_25proj.raw')):
    source_flatfield_folder = os.path.join(flatfield_projection_root_folder, phantom_type)
    copyfile(os.path.join(source_flatfield_folder,'flatfield_25proj.raw'), os.path.join(output_data_folder,'flatfield_25proj.raw'))
    # check whether the flatfield files are prepared
    mcgpu_folder = os.path.join(patient_folder,'mc_gpu')
    flatfield_files = glob.glob(os.path.join(mcgpu_folder,'flatfield*_0000.raw'))
    if len(flatfield_files) == 0:
        source_flatfield_files = glob.glob(os.path.join(source_flatfield_folder,'flatfield*_0000.raw'))
        target_flatfield_file = os.path.join(mcgpu_folder,'flatfield_{0:}_crop.raw.gz_0000.raw'.format(rand_seed))
        copyfile(source_flatfield_files[0], target_flatfield_file)  ## copy the DM flatfield to the mc_gpu folder

## Dimenion size extraction from mhd files
dim_x, dim_y, dim_z = 0, 0, 0
mhd_file = os.path.join(patient_folder,'pc_{}_crop.mhd'.format(rand_seed))
with open(mhd_file,'r+') as f:
    lines = f.readlines()
    for line in lines:
	splits = line.rstrip().split(' ')
	if splits[0] == 'DimSize':
	    dim_x, dim_y, dim_z = splits[-3], splits[-2], splits[-1]
	    print((dim_x, dim_y, dim_z))

## FBP DBT reconstruction
#FBP_cmd_folder = os.path.expanduser('~/05-VICTRE/FBP_DBT_reconstruction_in_C')
log_folder = os.path.join(patient_folder,'logs')
generate_folder(log_folder)
if isInserted:
    log_file = os.path.join(output_data_folder,'log_recon_insert.txt')
    time_file = os.path.join(log_folder,'time_DBT_recon_insert.txt')
else:
    log_file = os.path.join(output_data_folder,'log_recon_noninsert.txt')
    time_file = os.path.join(log_folder,'time_DBT_recon_noninsert.txt')
#myCmd = '{0:}/FBP_DBTrecon 25 3000 1500 0.0085 65.0 60.0 0.000 50.00 {1:} {2:} {3:} 0.0050 0.0085 0.1 0 -25.0 2.083333333333333333 {4:}'.format(FBP_cmd_folder,dim_y, dim_x, dim_z, rand_seed)
myCmd = '{0:}/FBP_DBTrecon_PRO 25 3000 1500 0.0085 65.0 60.0 0.000 50.00 {1:} {2:} {3:} 0.0050 0.0085 0.1 0 -25.0 2.083333333333333333 {4:} {5:}'.format(FBP_cmd_folder,dim_y, dim_x, dim_z, rand_seed, data_root_folder)
print(myCmd)
#os.system(myCmd)
results = subprocess.check_output(myCmd, shell=True)
with open(log_file,'w+') as f:
     f.write(results)

## copy the log file to a uniform log folder
recon_log_file = os.path.join(log_folder,os.path.basename(log_file))
copyfile(log_file, recon_log_file)

## obtain the dimensions of the recontructed DBT images
nx, ny, nz = 0, 0, 0
with open(log_file) as f:
     lines = f.readlines()
     for line in lines:
 	splits = line.rstrip().split(' ')
 	if splits[0] == 'nx':
 	    splits = re.split(r'[ ,;,\t]', line.rstrip())
 	    nx, ny, nz = splits[2], splits[6], splits[-1]
 	    print('DimSize: nx = {}, ny = {}, nz = {}'.format(splits[2], splits[6], splits[-1]))
 
size_file = os.path.join(output_data_folder,'DBT_recon_size.txt')
if not os.path.exists(size_file):
    with open(size_file, 'w+') as f:
        f.write('{}\n{}\n{}\n'.format(nx,ny,nz))
 
## rename the DBT file
dbt_recon_file = os.path.join(output_data_folder, 'DBT_{}_recon.raw'.format(rand_seed))
if isInserted:
    new_file_name = os.path.join(output_data_folder, 'pcl_DBT_{}_recon.raw'.format(rand_seed))
else:
    new_file_name = os.path.join(output_data_folder, 'pc_DBT_{}_recon.raw'.format(rand_seed))
os.rename(dbt_recon_file, new_file_name)
 
## ending time measured in hours
duration_time = (time.time() - start_time)/60/60
with open(time_file,'w+') as f:
    f.write('DBT reon time cost: {0:03f} hours\n'.format(duration_time))
