import os
import time
from shutil import copyfile
import glob

def generate_folder(folder):
        if not os.path.exists(folder):
                os.mkdir(folder)

phantom_set_folder = os.path.expanduser('~/08-Phantom_Set')
output_set_folder = os.path.expanduser('~/09-xray_images')

def xray_sync_check(phantom_set_folder=phantom_set_folder, output_set_folder=output_set_folder, random_seed = 121760580, insert_label = 'nl', signal_model_code = 0):
	phantom_data_folder = os.path.join(phantom_set_folder, str(random_seed))
	output_data_folder = os.path.join(output_set_folder, str(random_seed))
	generate_folder(output_data_folder)
	status_ready = False
	# the integrity of generated phantom data
	# print(phantom_data_folder)
	crop_data_file = os.path.join(phantom_data_folder,'pc_{}_crop.raw.gz'.format(random_seed))
	phantom_data_file = os.path.join(phantom_data_folder,'p_{}.raw.gz'.format(random_seed))
	compressed_data_file = os.path.join(phantom_data_folder,'pc_{}.raw.gz'.format(random_seed))
	crop_mhd_file = os.path.join(phantom_data_folder,'pc_{}_crop.mhd'.format(random_seed))
	local_file = os.path.join(phantom_data_folder,'pc_{}.loc'.format(random_seed))
# 	print(os.path.exists(crop_data_file))
# 	print(os.path.exists(phantom_data_file))
# 	print(os.path.exists(compressed_data_file))
# 	print(os.path.exists(crop_mhd_file))
# 	print(os.path.exists(local_file))
	phantom_integrity_check = os.path.exists(crop_data_file) and os.path.exists(phantom_data_file) and\
		os.path.exists(compressed_data_file) and os.path.exists(crop_mhd_file) and os.path.exists(local_file)
	print('integrity:{}'.format(phantom_integrity_check))
	flag_folder = os.path.join(output_data_folder,'status_flags')
	if insert_label == 'nl':
		flag_file = os.path.join(flag_folder, 'x-ray-not-insert-{}'.format(signal_model_code))
	elif insert_label == 'l':
		flag_file = os.path.join(flag_folder, 'x-ray-insert-{}'.format(signal_model_code))
	sleep_time = 1
	time.sleep(sleep_time)
	token_check = not os.path.exists(flag_folder) or not os.path.exists(flag_file)
	print('token_check:{}'.format(token_check))
	if phantom_integrity_check and token_check:
		print(flag_file)
		status_ready = True
		generate_folder(flag_folder)
		with open(flag_file, 'w+') as f:
			f.write('processing\n')
		if insert_label == 'nl':
			trg_crop_file = os.path.join(output_data_folder,'pc_{}_crop.raw.gz'.format(random_seed))
			trg_crop_mhd_file = os.path.join(output_data_folder,'pc_{}_crop.mhd'.format(random_seed))
			trg_local_file = os.path.join(output_data_folder,'pc_{}.loc'.format(random_seed))
			# prepare the data 
			copyfile(crop_data_file,trg_crop_file)
			copyfile(crop_mhd_file,trg_crop_mhd_file)
			copyfile(local_file,trg_local_file)
			phantom_lesion_folder = os.path.join(output_data_folder, 'phantom_l0')
		else:
			phantom_lesion_folder = os.path.join(output_data_folder, 'phantom_l{}'.format(signal_model_code))
		generate_folder(phantom_lesion_folder)
	else:
		phantom_lesion_folder = output_data_folder
	return status_ready, phantom_lesion_folder

def xray_generation_check(output_set_folder=output_set_folder, random_seed = 121760580, insert_label = 'nl', signal_model_code = 0):
	# phantom_data_folder = os.path.join(phantom_set_folder, str(random_seed))
	output_data_folder = os.path.join(output_set_folder, str(random_seed))
	# generate_folder(output_data_folder)
	gen_success = False
	mcgpu_data_folder = os.path.join(output_data_folder,'phantom_l{}'.format(signal_model_code),'mc_gpu')
	xray_file_ptrn = os.path.join(mcgpu_data_folder,'pc*.gz_00*.raw')
	xray_files = glob.glob(xray_file_ptrn)
	# print(xray_files)
	if len(xray_files) == 26:
		if insert_label == 'nl':
			print('X-ray imaging succeeds for signal-absent case!!')
		else:
			print('X-ray imaging succeeds for signal-present case!!')
		gen_success = True
	else:
		# remove token file and phantom
		os.system('rm -rf {}/phantom_l{}'.format(output_data_folder, signal_model_code))
		if insert_label == 'nl':
			flag_file_name = 'x-ray-not-insert-{}'.format(signal_model_code)
		else:
			flag_file_name = 'x-ray-insert-{}'.format(signal_model_code)
		os.system('rm {}/status_flags/{}'.format(output_data_folder, flag_file_name))
	return gen_success
