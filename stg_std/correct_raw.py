import sys
import numpy as np
from multiprocessing import cpu_count
import argparse

sys.path.append('../../')
sys.path.append("/home/minghao/stgrom/")
from stgrom import EOS_DATA, SUN_MASS, TSDensity, TSPoints, STGHandler
from stgrom import ExRaw

EOS_Range = {'AP3': [0.60e15, 0.73e15, 1.00e15, 1.13e15, 1.47e15, 1.54e15], #[1.03, 2.26]
             'AP4': [0.73e15, 0.89e15, 1.03e15, 1.13e15, 1.67e15, 2.44e15], #[0.95, 2.21]
             'ENG': [0.61e15, 0.75e15, 1.08e15, 1.30e15, 1.60e15, 2.12e15], #[1.02, 2.22]
              'H4': [0.40e15, 0.56e15, 1.04e15, 1.35e15, 2.00e15, 2.10e15], #[0.93, 2.03]
            'MPA1': [0.55e15, 0.68e15, 0.89e15, 1.06e15, 1.36e15, 1.53e15], #[1.01, 2.40]
            'PAL1': [0.40e15, 0.62e15, 0.87e15, 1.10e15, 1.49e15, 1.76e15], #[1.05, 2.35]
            'SLy4': [0.68e15, 0.87e15, 1.20e15, 1.54e15, 1.97e15, 2.70e15], #[1.00, 2.04]
            'WFF1': [0.92e15, 1.05e15, 1.28e15, 1.47e15, 1.85e15, 2.82e15], #[0.92, 2.13]
            'WFF2': [0.77e15, 0.92e15, 1.21e15, 1.39e15, 1.75e15, 2.42e15], #[0.97, 2.18]
          'BL_EOS': [0.60e15, 0.80e15, 1.20e15, 1.50e15, 1.90e15, 2.18e15], #[0.82, 2.05]
           'BSk20': [0.66e15, 0.80e15, 1.09e15, 1.40e15, 1.70e15, 2.04e15], #[0.84, 2.13]
           'BSk21': [0.53e15, 0.68e15, 0.94e15, 1.17e15, 1.50e15, 2.04e15], #[0.80, 2.24]
           'BSk22': [0.48e15, 0.67e15, 1.00e15, 1.23e15, 1.70e15, 1.92e15], #[0.90, 2.25]
           'BSk25': [0.55e15, 0.70e15, 0.95e15, 1.23e15, 1.90e15, 2.02e15], #[0.88, 2.22]
            'SLy9': [0.56e15, 0.70e15, 1.05e15, 1.34e15, 2.00e15, 2.10e15], #[0.90, 2.14]
         'SLy230a': [0.65e15, 0.85e15, 1.13e15, 1.44e15, 2.00e15, 2.30e15], #[0.85, 2.08]
}

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--label', type=str, default = None)
parser.add_argument('--EOS-name', type=str, default=None)
args = parser.parse_args()

label = args.label
EOS_name = args.EOS_name

if EOS_name not in EOS_Range.keys():
   raise Exception(">>> EOS_name Error")
# label = 'Task'

cpu_count = cpu_count()

# EOS_name = 'H4'

print('###CORRECT###')


def rawcorrect(raw,i=0):
    highss=[j+0.5 for j in range(50)]
    err_list, err_pool = raw.check('iter')
    print('rawcorrect: i:',i,'err:', len(err_list))
    print(err_list)
    print(err_pool)
    if err_list != []:
        raw.correct(err_list=err_list, err_pool=err_pool, threading=cpu_count, max_iter=50, high_s=highss[i], verbose=False)
    else:
        print("No Error")
    err_list, err_pool = raw.check('iter')
    #print('err:', len(err_list))
    for err in err_list:
        print(err,":",raw.data[err[0],err[1],err[2]])

def rawfill(raw):
    err_list, err_pool = raw.check('iter')
    #err_list, err_pool = raw.check('nan')
    print(err_list)
    print(err_pool)
    if err_list != []:
        raw.fill(err_list=err_list, err_pool=err_pool)
    else:
        print("No Error")
    raw.save('Cor')


#raw = LoadRaw(EOS_name=EOS_name, label=label)
raw = ExRaw(EOS_name=EOS_name, label='Task')
for i in range(15):
    rawcorrect(raw,i)
rawfill(raw)
#raw.exdata(threading=cpu_count,multip=True,label='Test')
#raw.exdata(threading=1,multip=False)
############################################################
#only fill
#raw = ExRaw(EOS_name=EOS_name, label='Cor')
#rawfill(raw)
print('Done.')
