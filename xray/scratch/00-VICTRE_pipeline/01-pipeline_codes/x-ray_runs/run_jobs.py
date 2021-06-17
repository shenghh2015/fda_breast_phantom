import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("gpu_num",type=int)		
args = parser.parse_args()

cmd = 'python run_xray_pipeline.py {}'.format(args.gpu_num)

nb_iter = 10000

for i in range(nb_iter):
	os.system(cmd)


