import os
import random
from shutil import copyfile
import re
import argparse
import time
import subprocess
import glob

################## command configuration  ################
roi_cmd_folder = os.path.expanduser('~/05-VICTRE/ROIExtraction')
template_flatfield_folder = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/03-DBTrecon_files/flatfield')

def generate_folder(folder):
	if not os.path.exists(folder):
		os.mkdir(folder)

# Parsing input arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument("RndSeed",type=int)		
parser.add_argument("phantom_type",type=str)  		
parser.add_argument("phantom_data_folder", type = str)
parser.add_argument("image_type",type=str) # image type: mamma or dbt
parser.add_argument("signal_case", type = str) # signal type: SP-> signal present or SA-> signal absent
args = parser.parse_args()

## start time
start_time = time.time()

rand_seed = args.RndSeed
phantom_type = args.phantom_type
image_type = args.image_type
data_root_folder = args.phantom_data_folder
signal_case = args.signal_case
# os.environ["CUDA_VISIBLE_DEVICES"] = args.GPU_number

# rand_seed = 1759166
# phantom_type = 'scattered'
# isInserted = True

# data_root_folder = os.path.expanduser('~/07-Datasets')
patient_folder = os.path.join(data_root_folder,'{}'.format(rand_seed))
output_data_folder = os.path.join(patient_folder,'roi_voi')
generate_folder(output_data_folder)

## the roi extraction command folder
#roi_cmd_folder = os.path.expanduser('~/05-VICTRE/ROIExtraction')

##  copy the DM flatfield projection
src_flatfield_ptrn = os.path.join(template_flatfield_folder,'{0:}/flatfield*_0000.raw'.format(phantom_type))
flatfield_files = glob.glob(src_flatfield_ptrn)
src_flatfield_file = flatfield_files[0]
trg_flatfield_file = os.path.join(patient_folder,'mc_gpu/flatfield_{0:}_crop.raw.gz_0000.raw'.format(rand_seed))
        
if not os.path.exists(trg_flatfield_file):
    copyfile(src_flatfield_file,trg_flatfield_file)

## copy the DBT flatfield projections
src_DBT_flatfield_file = os.path.join(template_flatfield_folder, '{0:}/flatfield_25proj.raw'.format(phantom_type))
trg_DBT_flatfield_file = os.path.join(patient_folder, 'dbt_recon/flatfield_25proj.raw')
if not os.path.exists(trg_DBT_flatfield_file):
    generate_folder(os.path.join(patient_folder, 'dbt_recon'))
    copyfile(src_DBT_flatfield_file, trg_DBT_flatfield_file)

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

## read the size of the DBT recon images
if image_type == 'dbt':
    dbt_size_file = os.path.join(patient_folder,'dbt_recon','DBT_recon_size.txt')
    nx, ny, nz = 0, 0 ,0
    val_list = []
    if os.path.exists(dbt_size_file):
	with open(dbt_size_file, 'r+') as f:
		lines = f.readlines()
		for line in lines:
			val_list.append(int(line.rstrip()))
	nx = val_list[0]
	ny = val_list[1]
	nz = val_list[2]

## generate the mammo and dbt folders
generate_folder(os.path.join(output_data_folder, 'mammo'))
generate_folder(os.path.join(output_data_folder,'dbt'))
generate_folder(os.path.join(output_data_folder,'loc'))

## log folder
log_folder = os.path.join(patient_folder, 'logs')
generate_folder(log_folder)

########################### ROI extraction #####################

if image_type == 'mammo' and signal_case == 'SA':
	phantom_folder = patient_folder
	mcgpu_image_folder = os.path.join(patient_folder,'mc_gpu')
	flatfield_file_folder = mcgpu_image_folder
	cal_output_folder = os.path.join(output_data_folder, 'mammo', 'microcal')
	mass_output_folder = os.path.join(output_data_folder,'mammo','mass')
	loc_output_folder = os.path.join(output_data_folder,'mammo','loc')
	generate_folder(cal_output_folder)
	generate_folder(mass_output_folder)
	generate_folder(loc_output_folder)
	log_file = os.path.join(log_folder, 'log_mammo_SA.txt')
	time_file = os.path.join(log_folder, 'time_mammo_SA.txt')
	extract_cmd = 'python {0:}/roiExtraction_mammo_SA.py {1:} 0 60.25 630 0 {2:} 0.085 {3:} {4:} {5:} 0 0 0 {6:} {7:} {8:} 65 109 1500 3000 -20 {9:} {10:} {11:} {12:} {13:} {14:}'.format(roi_cmd_folder, rand_seed, elementSpac, offsetX, offsetY, offsetZ, dimX, dimY, dimZ, phantom_folder, mcgpu_image_folder,flatfield_file_folder,cal_output_folder, mass_output_folder, loc_output_folder)

elif image_type == 'mammo' and signal_case == 'SP':
	## mammo ROI extraction for SP case
	phantom_folder = patient_folder
	mcgpu_image_folder = os.path.join(patient_folder,'mc_gpu')
	flatfield_file_folder = mcgpu_image_folder
	cal_output_folder = os.path.join(output_data_folder,'mammo','microcal')
	mass_output_folder = os.path.join(output_data_folder,'mammo','mass')
	loc_output_folder = os.path.join(output_data_folder,'mammo','loc')
	generate_folder(cal_output_folder)
	generate_folder(mass_output_folder)
	generate_folder(loc_output_folder)
	log_file = os.path.join(log_folder, 'log_mammo_SP.txt')
	time_file = os.path.join(log_folder,'time_mammo_SP.txt')
	extract_cmd = 'python {0:}/roiExtraction_mammo_SP.py {1:} 0 60.25 630 0 {2:} 0.085 {3:} {4:} {5:} 0 0 0 {6:} {7:} {8:} 65 109 1500 3000 -20 {9:} {10:} {11:} {12:} {13:} {14:}'.format(roi_cmd_folder, rand_seed, elementSpac, offsetX, offsetY, offsetZ, dimX, dimY, dimZ, phantom_folder, mcgpu_image_folder,flatfield_file_folder,cal_output_folder, mass_output_folder, loc_output_folder)

elif image_type == 'dbt' and signal_case == 'SA':
	## DBT ROV extraction for SA case
	phantom_folder = patient_folder
	recon_image_folder = os.path.join(patient_folder,'dbt_recon')
	flatfield_file_folder = os.path.join(patient_folder,'mc_gpu')
	cal_output_folder = os.path.join(output_data_folder,'dbt','microcal')
	mass_output_folder = os.path.join(output_data_folder,'dbt','mass')
	loc_output_folder = os.path.join(output_data_folder,'dbt','loc')
	generate_folder(cal_output_folder)
	generate_folder(mass_output_folder)
	generate_folder(loc_output_folder)
	## rename the DBT file
	dbt_data_file = os.path.join(recon_image_folder, 'pc_DBT_{}_recon.raw'.format(rand_seed))
	input_data_file = os.path.join(recon_image_folder, 'DBT_{}_recon.raw'.format(rand_seed))
	copyfile(dbt_data_file, input_data_file)
	log_file = os.path.join(log_folder, 'log_DBT_SA.txt')
	time_file = os.path.join(log_folder,'time_DBT_SA.txt')
	extract_cmd = 'python {0:}/roiExtraction_DBT_FBP_SA.py {1:} 0 60.25 630 0 {2:} {3:} {4:} 0.085 1 {5:} {6:} {7:} 0 0 0 65 109 5 9 2 2 4 4 {8:} {9:} {10:} {11:} {12:} {13:} {14:}'.format(roi_cmd_folder, rand_seed, nx, ny, nz, offsetX, offsetY, offsetZ, elementSpac, phantom_folder, recon_image_folder, flatfield_file_folder, cal_output_folder, mass_output_folder, loc_output_folder)

elif image_type == 'dbt' and signal_case == 'SP':
	## DBT ROV extraction for SP case
	phantom_folder = patient_folder
	recon_image_folder = os.path.join(patient_folder,'dbt_recon')
	flatfield_file_folder = os.path.join(patient_folder,'mc_gpu')
	cal_output_folder = os.path.join(output_data_folder,'dbt','microcal')
	mass_output_folder = os.path.join(output_data_folder,'dbt','mass')
	loc_output_folder = os.path.join(output_data_folder,'dbt','loc')
	generate_folder(cal_output_folder)
	generate_folder(mass_output_folder)
	generate_folder(loc_output_folder)
	## rename the DBT file
	dbt_data_file = os.path.join(recon_image_folder, 'pcl_DBT_{}_recon.raw'.format(rand_seed))
	input_data_file = os.path.join(recon_image_folder, 'DBT_{}_recon.raw'.format(rand_seed))
	copyfile(dbt_data_file, input_data_file)
	extract_cmd = 'python {0:}/roiExtraction_DBT_FBP_SP.py {1:} 0 60.25 630 0 {2:} {3:} {4:} 0.085 1 {5:} {6:} {7:} 0 0 0 65 109 5 9 2 2 4 4 {8:} {9:} {10:} {11:} {12:} {13:} {14:}'.format(roi_cmd_folder, rand_seed, nx, ny, nz, offsetX, offsetY, offsetZ, elementSpac, phantom_folder, recon_image_folder, flatfield_file_folder, cal_output_folder, mass_output_folder, loc_output_folder)
	log_file = os.path.join(log_folder, 'log_DBT_SP.txt')
	time_file = os.path.join(log_folder,'time_DBT_SP.txt')

## log the process
print(extract_cmd)
# os.system(extract_cmd)
results = subprocess.check_output(extract_cmd, shell = True)
with open(log_file,'w+') as f:
    f.write(results)

## duration time measured in hours
time_cost = (time.time()-start_time)/60/60
with open(time_file,'w+') as f:
    f.write('ROI/VOI extraction time cost:{0:.3f}\n'.format(time_cost))

