######################################################################################
### The python wrapped codes for X-ray imaging ##
### created by: Shenghua He ##
### Date: 09/26/2019 ##
######################################################################################

import os
import random
from shutil import copyfile
import argparse
import commands
import  subprocess
import time

################## directory configurations for MCGPU codes ########################
#data_root_folder = os.path.expanduser('~/00-VICTRE_pipeline/02-phantom_set')
cfg_folder = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/02-mcgpu_files/cfg')
mcgpu_cmd_folder = os.path.expanduser('~/04-VICTRE_MCGPU')

def generate_folder(folder):
	if not os.path.exists(folder):
		os.mkdir(folder)

# Parsing input arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument("RndSeed",type=int)             # specify random seed
parser.add_argument("phantom_type",type=str)        # specify phantom type
parser.add_argument("phantom_data_folder",type=str) # specify phantom data folder
parser.add_argument('GPU_number', type = int)       # specify which GPU to use
parser.add_argument('mass_density', type = float)   # specify the density of signal to decide which version of CUDA codes to use
parser.add_argument('inserted', type = int)         # specify whether to insert 
parser.add_argument('isFlatfield', type = int)      # specify whether to generate the flatfield files
args = parser.parse_args()

#os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# rand_seed = 1759166
# phantom_type = 'scattered'

## start time
start_time = time.time()

rand_seed = args.RndSeed
phantom_type = args.phantom_type
data_root_folder = args.phantom_data_folder
mass_density = args.mass_density
isFlatfield = args.isFlatfield
os.environ["CUDA_VISIBLE_DEVICES"] = '{}'.format(args.GPU_number)

print(args.inserted)
isInserted = bool(args.inserted)
# isInserted = True
#data_root_folder = os.path.expanduser('~/07-Datasets')
patient_folder = os.path.join(data_root_folder,'{}'.format(rand_seed))
output_data_folder = os.path.join(patient_folder,'mc_gpu')
generate_folder(output_data_folder)

### x-ray imaging configuration
#cfg_folder = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/02-mcgpu_files/cfg')
src_cfg_file = os.path.join(cfg_folder,'{}.in'.format(phantom_type))
trg_cfg_file = os.path.join(output_data_folder,'{}.in'.format(phantom_type))
copyfile(src_cfg_file,trg_cfg_file)

dim_x, dim_y, dim_z = 0, 0, 0
off_x, off_y, off_z = 0, 0, 0

print(isInserted)

if not isInserted:
	phantom_data_file = os.path.join(patient_folder,'pc_{}_crop.raw.gz'.format(rand_seed))
	mhd_file = os.path.join(patient_folder,'pc_{}_crop.mhd'.format(rand_seed))
	mcgpu_file_header = os.path.join(output_data_folder,'pc_{}_crop.raw.gz'.format(rand_seed))
else:
	phantom_data_file = os.path.join(patient_folder,'pcl_{}_crop.raw.gz'.format(rand_seed))
	mhd_file = os.path.join(patient_folder,'pc_{}_crop.mhd'.format(rand_seed))
	mcgpu_file_header = os.path.join(output_data_folder,'pcl_{}_crop.raw.gz'.format(rand_seed))

print(phantom_data_file)
print(mcgpu_file_header)

with open(mhd_file,'r+') as f:
	lines = f.readlines()
	for line in lines:
		splits = line.rstrip().split(' ')
		if splits[0] == 'DimSize':
			dim_x, dim_y, dim_z = splits[-3], splits[-2], splits[-1]
			print((dim_x, dim_y, dim_z))
		if splits[0] == 'Offset':
			off_x, off_y, off_z = float(splits[-3])/10, float(splits[-2])/10, float(splits[-1])/10
			print((off_x, off_y, off_z))

dimSize_str = '{} {} {}'.format(dim_x, dim_y, dim_z)
off_str = '{} {} {}'.format(off_x, off_y, off_z)

## X ray configuration files
with open(trg_cfg_file,'r+') as f:
	lines = f.readlines()
	for i, line in enumerate(lines):
		if line.rstrip()  == '#[SECTION IMAGE DETECTOR v.2017-06-20]':
			if isFlatfield == 0:
				lines[i+1] = mcgpu_file_header+' # OUTPUT IMAGE FILE NAME\n'
			else:
				lines[i+1] = os.path.join(output_data_folder,'flatfield_{}_crop.raw.gz'.format(rand_seed))+' # OUTPUT IMAGE FILE NAME\n'
		splits = line.rstrip().split('#')
		if splits[-1] == ' VOXEL GEOMETRY FILE (penEasy 2008 format; .gz accepted)':
			if isFlatfield == 1:
				lines[i+1] = '999.0 0.0 0.0' + ' # OFFSET OF THE VOXEL GEOMETRY (DEFAULT ORIGIN AT LOWER BACK CORNER) [cm]\n'
				print(lines[i+1])
		if splits[-1] == ' OFFSET OF THE VOXEL GEOMETRY (DEFAULT ORIGIN AT LOWER BACK CORNER) [cm]':
			lines[i+1] = dimSize_str+' # NUMBER OF VOXELS: INPUT A 0 TO READ ASCII FORMAT WITH HEADER SECTION, RAW VOXELS WILL BE READ OTHERWISE\n'
			print(lines[i+1])
# 		elif splits[-1] == ' VOXEL GEOMETRY FILE (penEasy 2008 format; .gz accepted)':
# 			if isFlatfield == 1:
# 				lines[i+1] = '999.0 0.0 0.0'+' # OFFSET OF THE VOXEL GEOMETRY (DEFAULT ORIGIN AT LOWER BACK CORNER) [cm]\n'
# 				print(lines[i+1])
		if line.rstrip() == '#[SECTION VOXELIZED GEOMETRY FILE v.2017-07-26]':
			lines[i+1] = phantom_data_file+' # VOXEL GEOMETRY FILE (penEasy 2008 format; .gz accepted)\n'

os.remove(trg_cfg_file)
with open(trg_cfg_file,'a') as f:
	f.writelines(lines)

### X-ray imaging
#mcgpu_cmd_folder = os.path.expanduser('~/04-VICTRE_MCGPU')
#myCmd = '{0:}/MC-GPU_v1.5b.x {1:}'.format(mcgpu_cmd_folder, trg_cfg_file)
myCmd = '{0:}/MC-GPU_v1.5b.x_{1:} {2:}'.format(mcgpu_cmd_folder, mass_density, trg_cfg_file)
print(myCmd)
#os.system(myCmd)
results = subprocess.check_output(myCmd, shell = True)
log_folder = os.path.join(patient_folder, 'logs')
generate_folder(log_folder)
if isInserted:
    log_file = os.path.join(log_folder, 'log_xray_insert.txt')
    time_file = os.path.join(log_folder,'time_xray_insert.txt')
else:
    log_file = os.path.join(log_folder, 'log_xray_noninsert.txt')
    time_file = os.path.join(log_folder,'time_xray_noninsert.txt')
with open(log_file,'w+') as f:
        f.write(results)

## duration time 
time_cost = (time.time()-start_time)/60/60
with open(time_file,'w+') as f:
    f.write('Xray time cost: {0:} hours\n'.format(time_cost))
    
