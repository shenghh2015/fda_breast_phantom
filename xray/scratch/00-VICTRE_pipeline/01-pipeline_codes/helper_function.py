import os
import numpy as np
import glob
import argparse
import random

#parser = argparse.ArgumentParser()
#parser.add_argument('--machine_number',type=int)
#args = parser.parse_args()

#machine_number = args.machine_number


#rand_seed_file = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/00-rand_seed/rand_seed.txt')
#rand_seed_folder = '/shared/aristotle/Phantom/00-VICTRE_pipeline/00-base_input_files/00-rand_seed'
rand_seed_folder = '/scratch/00-VICTRE_pipeline/00-base_input_files/00-rand_seed'
#machine_number = 8
#initial_seed = 1000

def generate_folder(folder):
        if not os.path.exists(folder):
                os.mkdir(folder)

def rand_seed_gen():
# 	rand_seed_folder = os.path.expanduser('~/00-VICTRE_pipeline/00-base_input_files/00-rand_seed')
	generate_folder(rand_seed_folder)
	rand_seed_file = os.path.join(rand_seed_folder,'rand_seed.txt')

	max_rand = 9999999  # 7-digit random seeds
	number_of_patients = 300000

	## Generate a certain number of random seeds for phantom generation
	#random.seed(initial_seed)
	random_seeds = random.sample(range(max_rand),number_of_patients)
	np.savetxt(rand_seed_file, random_seeds, delimiter=',')

def rand_seed_fetch_v1(machine_number, dataset_root_folder, phantom_type = 'dense'):
# 	phantom_type = 'dense'
# 	dataset_root_folder = '/home/shenghua/07-Datasets'
	patient_list = []  ## put the random_seed in the patient folder in a list
	files = glob.glob(os.path.join(dataset_root_folder, '*'))
	for file in files:
		if os.path.isdir(file):
			read_seed = int(os.path.basename(file))
			read_seed = read_seed%10000000
			patient_list.append(read_seed)

	## 
	generate_folder(rand_seed_folder)
	rand_seed_file = os.path.join(rand_seed_folder,'rand_seed.txt')
	if not os.path.exists(rand_seed_file):
		rand_seed_gen()

	# read the rand_seed file
	rand_seed_arr = np.loadtxt(rand_seed_file, np.int32, ',')
	rand_seeds = rand_seed_arr
# 	if phantom_type == 'dense':
# 		rand_seeds = rand_seed_arr[0::4]
# 	elif phantom_type == 'hetero':
# 		rand_seeds = rand_seed_arr[1::4]
# 	elif phantom_type == 'scattered':
# 		rand_seeds = rand_seed_arr[2::4]
# 	elif phantom_type == 'fatty':
# 		rand_seeds = rand_seed_arr[3::4]

	# fetch a random seed from the rand_seed arry
	fetched_seed = 0
	for i in range(rand_seeds.shape[0]):
		seed = rand_seeds[i]
		if not seed in patient_list:
			fetched_seed = seed
			break
		else:
			continue

	if fetched_seed == 0:
		print('The random seeds are out of stock!!')

	if phantom_type == 'dense':
		fetched_seed = fetched_seed + 10000000
	elif phantom_type == 'hetero':
		fetched_seed = fetched_seed + 20000000
	elif phantom_type == 'scattered':
		fetched_seed = fetched_seed + 30000000		
	elif phantom_type == 'fatty':
		fetched_seed = fetched_seed + 40000000

	fetched_seed = np.int32(fetched_seed + machine_number*100000000)  ## machine id is different on different machine

	return fetched_seed
