#!/home/mdi0316/anaconda3/bin/python

import os, re, sys
import random
from random import randint
from itertools import cycle
import shutil
import math 
import subprocess as sp

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


scripts_dir = '/home/mdi0316/FUNCTIONS'
classes_dir = '/home/mdi0316/CLASSES'
sys.path.insert(0, scripts_dir)
sys.path.insert(0, classes_dir)

from Functions import print_tab, running_jobs, find_last_log
run_ids, run_labels, run_status = running_jobs()

from run_visco import make_label, make_new_folder, work_dir 

def main():
  data_df = pd.DataFrame(columns=[ 'exp', 'nat', 'Temp', 'status', 'dens.ave', 'visco.ave'])
  for tmp_exp in range(7):
    for nat in [20, 40, 80]:
      for temp in [200, 400, 600]:
  
        tmp_label = make_label( temp, tmp_exp, nat )
        tmp_dir   = make_new_folder( temp, tmp_exp, nat )
        if tmp_label in run_labels:
           status='running'
        else:
           status='completed'
        input_file = os.path.join( tmp_dir, 'viscosity_CG.IL.in' )
        densi_file = os.path.join( tmp_dir, 'density.dat' )
        visco_file = os.path.join( tmp_dir, 'visco.dat' )
        densi_ave = float('nan')
        visco_ave = float('nan')
        if os.path.exists( densi_file ):
           densi_arr = np.array([ float(line.split()[2]) for line in open(densi_file, 'r').readlines()[1:] ])
           densi_ave = np.average( densi_arr )
        else:
           densi_ave = 'missing'
        if os.path.exists( visco_file ):
           visco_arr = np.array([ float(line.split()[6]) for line in open(visco_file, 'r').readlines()[1:] ])
           visco_ave = np.average( visco_arr )
        else:
           visco_ave = 'missing'
        data_df  = data_df.append( pd.Series( { 'exp' : tmp_exp, 'nat' : nat , 'Temp' : temp, 'status' : status,\
                                                'dens.ave' : densi_ave, 'visco.ave' : visco_ave} ), ignore_index=True )
  print(data_df)
  data_df.to_csv('transport.csv'.format(tmp_dir))
#fig = plt.figure()
#ax = fig.add_subplot(111)
#for m in m_list:
#  fix_df = visco_df.loc[ visco_df['m'] == m ]
#  if not fix_df.empty:
#    fix_df.plot( x='T', y='visco.ave', label=m, ax=ax)
#
#plt.show()
 
if __name__ == '__main__':
  main()

