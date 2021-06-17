import os
import glob

dataset_folder = os.path.expanduser('~/08-Phantom_Set')
codes_folder = os.path.expanduser('~/00-VICTRE_pipeline/01-pipeline_codes')

phantom_folders = glob.glob(dataset_folder+'/*')

output_file = os.path.join(codes_folder, 're_compression_list.txt')

with open(output_file, 'w+') as f:	
	for i, folder in enumerate(phantom_folders):
		random_seed = np.int32(os.path.basename(folder))
		print(random_seed)
		f.write('{}\n'.format(random_seed))
