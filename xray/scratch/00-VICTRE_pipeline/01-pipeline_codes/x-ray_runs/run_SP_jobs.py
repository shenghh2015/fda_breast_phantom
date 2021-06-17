import os
import argparse

#os.chdir('/scratch/00-VICTRE_pipeline/00-base_input_files/x-ray_runs/')

parser = argparse.ArgumentParser()
parser.add_argument("--num_jobs",type=int)		
parser.add_argument("--gpu_num",type=int)		
args = parser.parse_args()

path = os.getcwd()
print('The current path:{}'.format(path))

os.chdir('/scratch/00-VICTRE_pipeline/01-pipeline_codes/x-ray_runs')
cmd = 'python2 run_xray_SP.py {}'.format(args.gpu_num)

#cmd = 'python2 /scratch/00-VICTRE_pipeline/01-pipeline_codes/x-ray_runs/run_xray_SP.py {}'.format(args.gpu_num)

#nb_iter = 10000

nb_iter = args.num_jobs

for i in range(nb_iter):
	os.system(cmd)


