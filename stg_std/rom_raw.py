import sys
import numpy as np
from multiprocessing import cpu_count
import argparse

sys.path.append('../../')
sys.path.append("/home/minghao/stgrom/")
from stgrom import EOS_DATA, SUN_MASS, TSDensity, TSPoints, STGHandler
from stgrom import ExRaw
from stgrom.rosmm import  BuildROMm

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


EOS_Range_bur = {'AP3': [0.60e15, 0.79e15, 1.00e15, 1.13e15, 1.47e15, 1.54e15], #[1.03, 2.26]
             'AP4': [0.73e15, 0.89e15, 1.03e15, 1.13e15, 1.67e15, 2.44e15], #[0.95, 2.21]
             'ENG': [0.61e15, 0.75e15, 1.08e15, 1.30e15, 1.60e15, 2.12e15], #[1.02, 2.22]
              'H4': [0.40e15, 0.56e15, 1.04e15, 1.35e15, 2.00e15, 2.10e15], #[0.93, 2.03]
            'MPA1': [0.55e15, 0.68e15, 0.89e15, 1.06e15, 1.36e15, 1.53e15], #[1.01, 2.40]
            'PAL1': [0.40e15, 0.62e15, 0.87e15, 1.10e15, 1.49e15, 1.76e15], #[1.05, 2.35]
            'SLy4': [0.68e15, 0.87e15, 1.20e15, 1.54e15, 1.97e15, 2.70e15], #[1.00, 2.04]
            'WFF1': [0.92e15, 1.05e15, 1.28e15, 1.47e15, 1.85e15, 2.82e15], #[0.92, 2.13]
            'WFF2': [0.77e15, 0.92e15, 1.21e15, 1.39e15, 1.75e15, 2.42e15], #[0.97, 2.18]
          'BL_EOS': [0.60e15, 0.85e15, 1.20e15, 1.50e15, 1.90e15, 2.18e15], #[0.82, 2.05]
           'BSk20': [0.66e15, 0.80e15, 1.09e15, 1.40e15, 1.70e15, 2.04e15], #[0.84, 2.13]
           'BSk21': [0.53e15, 0.68e15, 0.94e15, 1.17e15, 1.50e15, 2.04e15], #[0.80, 2.24]
           'BSk22': [0.48e15, 0.67e15, 1.00e15, 1.23e15, 1.70e15, 1.92e15], #[0.90, 2.25]
           'BSk25': [0.55e15, 0.70e15, 0.95e15, 1.23e15, 1.90e15, 2.02e15], #[0.88, 2.22]
            'SLy9': [0.56e15, 0.70e15, 1.05e15, 1.34e15, 2.00e15, 2.10e15], #[0.90, 2.14]
         'SLy230a': [0.65e15, 0.85e15, 1.13e15, 1.44e15, 2.00e15, 2.30e15], #[0.85, 2.08]
}


EOS_bur_para = {'AP3': {'method':'log',      'a':1.0,    'x0':1.0}, 
                'AP4': {'method':'log',      'a':1.0,    'x0':1.0}, 
                'ENG': {'method':'log',      'a':1.0,    'x0':1.0}, 
                 'H4': {'method':'loglike',  'a':1.0,    'x0':0.2}, 
               'MPA1': {'method':'log',      'a':1.0,    'x0':1.0}, 
               'PAL1': {'method':'loglike',  'a':1.0,    'x0':0.2}, 
               'SLy4': {'method':'loglike',  'a':1.0,    'x0':0.2}, 
               'WFF1': {'method':'log',      'a':1.0,    'x0':1.0}, 
               'WFF2': {'method':'log',      'a':1.0,    'x0':1.0}, 
             'BL_EOS': {'method':'loglike',  'a':1.0,    'x0':0.2}, 
              'BSk20': {'method':'log',      'a':1.0,    'x0':1.0}, 
              'BSk21': {'method':'log',      'a':1.0,    'x0':1.0}, 
              'BSk22': {'method':'loglike',  'a':1.0,    'x0':0.2}, 
              'BSk25': {'method':'log',      'a':1.0,    'x0':1.0}, 
               'SLy9': {'method':'loglike',  'a':1.0,    'x0':0.2}, 
            'SLy230a': {'method':'loglike',  'a':1.0,    'x0':0.2}, 
}

EOS_rosm_dat_fmt= {'AP3': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
                'AP4': {'logkA':{'fmt':'log',      'a':1.0,    'x0':0.0},},
                #'AP4': {'logkA':{'fmt':'loglike',      'a':1.0,    'x0':1e-3},},
                'ENG': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
                 'H4': {'logkA':{'fmt':'loglike',  'a':1.0,    'x0':0.2},},
               'MPA1': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
               'PAL1': {'logkA':{'fmt':'loglike',  'a':1.0,    'x0':0.2},},
               'SLy4': {'logkA':{'fmt':'loglike',  'a':1.0,    'x0':0.2},},
               'WFF1': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
               'WFF2': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
             'BL_EOS': {'logkA':{'fmt':'loglike',  'a':1.0,    'x0':0.2},},
              'BSk20': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
              'BSk21': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
              'BSk22': {'logkA':{'fmt':'loglike',  'a':1.0,    'x0':0.2},},
              'BSk25': {'logkA':{'fmt':'log',      'a':1.0,    'x0':1.0},},
               'SLy9': {'logkA':{'fmt':'loglike',  'a':1.0,    'x0':0.2},},
            'SLy230a': {'logkA':{'fmt':'loglike',  'a':1.0,    'x0':0.2},},
}


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--label', type=str, default = None)
parser.add_argument('--EOS-name', type=str, default=None)
args = parser.parse_args()

label = args.label
EOS_name = args.EOS_name

if EOS_name not in EOS_Range.keys():
   raise Exception(">>> EOS_name Error")

label = 'Rom'
path = './'
cpu_count = cpu_count()

# EOS_name = 'H4'

print('###ROM###')

# burf,cut&save
#'''
ex = ExRaw(path=path,label='Ex', EOS_name=EOS_name)
burp=EOS_bur_para[EOS_name]
ex.burp=burp
ex.meta['burp']=burp
ex.burf(11)
xmark = ex.meta['e_cs']['interval'].copy()
#xmark[1] *= 1.08
xmark = EOS_Range_bur[EOS_name]
ex.burf(12,method=burp['method'],times=20,xmark=xmark,loglike_x0=burp['x0'])
print('burf')
ex.cutsave(begs=[6,5],ends=[6,5],label=label,path=path)
#'''

rosm = BuildROMm(EOS_name=EOS_name, label=label,path=path)
rosm.train_data_fmt.update(EOS_rosm_dat_fmt[EOS_name])
print(rosm.data.shape)
print(np.where(rosm.data==0))
print(np.where(rosm.data[:,:,:,11]==0))

numset = int(2.5 * len(rosm.e_cs))
rosm.training_init(num=numset, s_logAlphaA=0.01, s_logbetaA=0.01, s_logkA=0.0)
rosm.training(key='mA',seed=0, tol=1e-7, verbose=False)
rosm.training(key='R',seed=0, tol=1e-7, verbose=False)
rosm.training(key='logAlphaA',seed=0, tol=1e-5, verbose=False)
print('betaA')
rosm.training(key='logbetaA',seed=0, tol=1e-4, verbose=False)
print('kA')
rosm.training(key='logkA',seed=0, tol=1e-4, verbose=False)
print('IA')
rosm.training(key='logIA',seed=0, tol=1e-7, verbose=False)
rosm.saveModel(label=label)

print('Done.')
