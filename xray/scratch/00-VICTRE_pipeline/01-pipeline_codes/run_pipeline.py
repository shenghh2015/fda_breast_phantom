from helper_function import *
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument('--machine_number',type=int)
parser.add_argument('--phantom_type', type=str)
args = parser.parse_args()

machine_number = args.machine_number


## Directory for phantom output
dataset_root_folder = '/scratch/08-Phantom_Set'  ## phantom output folder

## configurations for job running
num_phantom = 1
phantom_type = args.phantom_type

######################### pipeline starts #########################

for i in range(num_phantom):
    # 9-digit random seed fetch
    fetch_seed = rand_seed_fetch_v1(machine_number, dataset_root_folder, phantom_type = phantom_type)
    # phantom generation
    gen_cmd = 'python phantom_gen.py {0:} {1:} {2:}'.format(fetch_seed, phantom_type, dataset_root_folder)
    print(gen_cmd)
    os.system(gen_cmd)

    # phantom compression and cropping
    comp_crop_cmd = 'python phantom_compress_crop.py {0:} {1:} {2:}'.format(fetch_seed, phantom_type, dataset_root_folder)
    print(comp_crop_cmd)
    os.system(comp_crop_cmd)


# for i in range(num_phantom):
# 	start_time = time.time()
# 	fetch_seed = rand_seed_fetch_v1(dataset_root_folder, phantom_type = phantom_type)
# 	
# 	## phantom generation
# 	gen_cmd = 'python phantom_gen.py {0:} {1:} {2:} {3:}'.format(fetch_seed, phantom_type, )
# 	print(gen_cmd)
# 	os.system(gen_cmd)
# 	gen_time = (time.time() - start_time)/60/60
# 
# 	
# 	with open(os.path.join(dataset_root_folder, '{}/phantom_gen_time.txt'.format(fetch_seed)),'w+') as f:
# 		f.write('Phantom gen time: {0:.3f} hours\n'.format(gen_time))
# 	comp_crop_cmd = 'python phantom_compress_crop.py {0:} {1:}'.format(fetch_seed, phantom_type)
# 	print(comp_crop_cmd)
# 	os.system(comp_crop_cmd)
# 	gen_comp_crop_time = (time.time() - start_time)/60/60
# 	with open(os.path.join(dataset_root_folder, '{}/gen_comp_crop_time.txt'.format(fetch_seed)),'w+') as f:
# 		f.write('Phantom gen time: {0:.3f} hours\n'.format(gen_comp_crop_time))
# 	insert_cmd = 'python lesion_insert.py {0:} {1:}'.format(rand_seed, phantom_type)
# 	print(insert_cmd)
# 	os.system(insert_cmd)
# 	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(rand_seed, phantom_type, num_GPU, 10.06, 0, 0)
# 	print(xray_cmd)
# 	os.system(xray_cmd)
# 	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(rand_seed, phantom_type, num_GPU, 10.06, 1, 0)
# 	print(xray_cmd)
# 	os.system(xray_cmd)
# 	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(rand_seed, phantom_type, num_GPU, 10.06, 1, 1)
# 	print(xray_cmd)
# 	os.system(xray_cmd)
# 	mammoROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 'mammo')
# 	print(mammoROI_cmd)
# 	os.system(mammoROI_cmd)
# 	dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 0)
# 	print(dbt_cmd)
# 	os.system(dbt_cmd)
# 	dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 1)
# 	print(dbt_cmd)
# 	os.system(dbt_cmd)
# 	dbtROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 'dbt')
# 	print(dbtROI_cmd)
# 	os.system(dbtROI_cmd)
# 	end_time = time.time()
# 	exec_time = (end_time - start_time)/60/60
# 	exec_times.append(exec_time)
# 	with open('execute_time_hetero.txt','w+') as f:
# 		for i, exe_t in enumerate(exec_times):
# 			f.write('Patient Number {0:}->exectutime time:{1:.3f} hours\n'.format(i,exe_t))
