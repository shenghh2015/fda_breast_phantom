import os
import time
from shutil import copyfile
import glob

output_set_folder = os.path.expanduser('/scratch/xray_set/03-xray_set')

def consistency_dbt_check(xray_set_folder = output_set_folder, random_seed = 121760580, insert_label = 'nl'):
    CONSISTENCY_FLAG = False
    phantom_folder = os.path.join(xray_set_folder,'{}'.format(random_seed))
    mhd_file = phantom_folder + '/pc_{}_crop.mhd'.format(random_seed)
    if insert_label == 'nl':
        xray_ptrn = os.path.join(phantom_folder, 'phantom_l0', 'mc_gpu', 'pc_*.raw')
        flag_file = os.path.join(phantom_folder,'status_flags/dbt_noninsert.txt')
    else:
        xray_ptrn = os.path.join(phantom_folder, 'phantom_l1','mc_gpu','pcl_*.raw')
        flag_file = os.path.join(phantom_folder,'status_flags/dbt_insert.txt')
    xrayfiles = glob.glob(xray_ptrn)
    if os.path.exists(mhd_file) and len(xrayfiles)==26 and not os.path.exists(flag_file):
        CONSISTENCY_FLAG = True

    return CONSISTENCY_FLAG