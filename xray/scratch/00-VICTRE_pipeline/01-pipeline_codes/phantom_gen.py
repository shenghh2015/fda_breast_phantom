import os
import random
from shutil import copyfile
import argparse
import time

################## command configuration #################
#phantom_cfg_folder = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/01-phantom_cfg')
phantom_cfg_folder = os.path.expanduser('/scratch/00-VICTRE_pipeline/00-base_input_files/01-phantom_cfg')
#breastPhantom_cmd_folder = os.path.expanduser('~/01-breastPhantom')
breastPhantom_cmd_folder = os.path.expanduser('/scratch/01-breastPhantom')

def generate_folder(folder):
	if not os.path.exists(folder):
		os.mkdir(folder)

# Parsing input arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument("RndSeed",type=int)			# random seed taken from phantom file name
parser.add_argument("phantom_type",type=str)  		# focal spot locations X,Y,Z (mm)
parser.add_argument("phantom_data_folder", type = str)  # the folder where phantom generation c codes are 

args = parser.parse_args()

phantom_type = args.phantom_type
rand_seed = args.RndSeed
dataset_root_folder = args.phantom_data_folder

start_time = time.time()   # start timestamp

# generate a patient folder in the output dataset folder
patient_folder = os.path.join(dataset_root_folder,'{}'.format(rand_seed))
generate_folder(patient_folder)

## copy a phantom configuration file to the created folder
src_cfg_file = os.path.join(phantom_cfg_folder,'VICTRE_{}.cfg'.format(phantom_type))
trg_cfg_file = os.path.join(patient_folder,'VICTRE_{}.cfg'.format(phantom_type))
copyfile(src_cfg_file,trg_cfg_file)

# phantom configuration
lines = []
with open(trg_cfg_file,"r+") as f:
	lines = f.readlines()
	for i, line in enumerate(lines):
		if line.rstrip() == '# output directory':
			lines[i+1] = 'outputDir={}\n'.format(patient_folder)
			print(lines[i+1])
		if line.rstrip() == '# chosen randomly if not set':
			print(lines[i+1])
			lines[i+1] = 'seed={}\n'.format(rand_seed)

os.remove(trg_cfg_file)
with open(trg_cfg_file,'a') as f:
	f.writelines(lines)

# phantom generation process
myCmd = '{0:}/breastPhantom -c {1:}'.format(breastPhantom_cmd_folder,trg_cfg_file)
print(myCmd)
os.system(myCmd)

## statistics and log
log_statistics_folder = os.path.join(patient_folder,'logs')
generate_folder(log_statistics_folder)

gen_time = (time.time() - start_time)/60/60
with open(os.path.join(dataset_root_folder, '{}/logs/time_phantom_gen.txt'.format(rand_seed)),'w+') as f:
	f.write('Phantom gen time: {0:.3f} hours\n'.format(gen_time))
