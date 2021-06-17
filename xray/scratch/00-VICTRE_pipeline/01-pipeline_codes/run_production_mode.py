from helper_function import *
import os
import time

# rand_seed = 1759164
# phantom_type = 'dense'
# rand_seed = 1759165
# phantom_type = 'hetero'
# rand_seed = 1759166
# phantom_type = 'scattered'
# rand_seed = 1759167
# phantom_type = 'fatty'
dataset_root_folder = os.path.expanduser('~/07-Datasets')
# rand_seed = rand_seed_fetch(phantom_type, dataset_root_folder)

# rand_seed = 3000001
# phantom_type = 'hetero'

# rand_seed = 3000002
#phantom_type = 'scattered'

#phantom_type = 'fatty'

#num_GPU = 3

# if phantom_type == 'dense':
# 	num_GPU = 0
# elif phantom_type == 'hetero':
# 	num_GPU = 1
# elif phantom_type == 'scattered':
# 	num_GPU = 2
# elif phantom_type == 'fatty':
# 	num_GPU = 3

#rand_seed_pools = [3000003, 3000004, 3000005]
#rand_seed_pools = [5000001]
exec_times = []
#rand_seed_pools = [1700003, 1700004]
#phantom_type_set = ['scattered', 'fatty']
#num_GPU = 0
rand_seed_pools = [1700002, 1700001]
phantom_type_set = ['hetero', 'dense']
num_GPU = 2

for idx in range(len(rand_seed_pools)):
        phantom_type = phantom_type_set[idx]
        rand_seed = rand_seed_pools[idx]
        print('Random seed:{0:}, Phantom type: {1:}'.format(rand_seed, phantom_type))
        ## start timestamp
	start_time = time.time()
	## prepare a script for running the pipeline
	gen_cmd = 'python phantom_gen.py {0:} {1:}'.format(rand_seed, phantom_type)
	print(gen_cmd)
	os.system(gen_cmd)
	comp_crop_cmd = 'python phantom_compress_crop.py {0:} {1:}'.format(rand_seed, phantom_type)
	print(comp_crop_cmd)
	os.system(comp_crop_cmd)
	insert_cmd = 'python lesion_insert.py {0:} {1:}'.format(rand_seed, phantom_type)
	print(insert_cmd)
	os.system(insert_cmd)
	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(rand_seed, phantom_type, num_GPU, 10.06, 0, 0)
	print(xray_cmd)
	os.system(xray_cmd)
	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(rand_seed, phantom_type, num_GPU, 10.06, 1, 0)
	print(xray_cmd)
	os.system(xray_cmd)
	xray_cmd = 'python MCGPU.py {0:} {1:} {2:} {3:} {4:} {5:}'.format(rand_seed, phantom_type, num_GPU, 10.06, 1, 1)
	print(xray_cmd)
	os.system(xray_cmd)
	mammoROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 'mammo')
	print(mammoROI_cmd)
	os.system(mammoROI_cmd)
	dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 0)
	print(dbt_cmd)
	os.system(dbt_cmd)
	dbt_cmd = 'python DBTrecon.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 1)
	print(dbt_cmd)
	os.system(dbt_cmd)
	dbtROI_cmd = 'python ROI_extraction.py {0:} {1:} {2:}'.format(rand_seed, phantom_type, 'dbt')
	print(dbtROI_cmd)
	os.system(dbtROI_cmd)
	end_time = time.time()
	exec_time = (end_time - start_time)/60/60
	exec_times.append(exec_time)
	with open('execute_time_hetero.txt','w+') as f:
		for i, exe_t in enumerate(exec_times):
			f.write('Patient Number {0:}->exectutime time:{1:.3f} hours\n'.format(i,exe_t))
	
