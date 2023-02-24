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

from 

work_dir = os.getcwd()

T_list = [ '300', '400', '500' ]


data_df = pd.DataFrame(columns=['T', 'dens.ave', 'visco.ave'])

for T in T_list:
  densi_file = os.path.join( work_dir, 'VISCO', 'T_{}'.format(T), 'seed_0', 'density.dat' )
  visco_file = os.path.join( work_dir, 'VISCO', 'T_{}'.format(T), 'seed_0', 'visco.dat' )
  densi_ave = float('nan')
  visco_ave = float('nan')
  if os.path.exists( densi_file ):
     densi_arr = np.array([ float(line.split()[2]) for line in open(densi_file, 'r').readlines()[1:] ])
     densi_ave = np.average( densi_arr )
  if os.path.exists( visco_file ):
     visco_arr = np.array([ float(line.split()[6]) for line in open(visco_file, 'r').readlines()[1:] ])
     visco_ave = np.average( visco_arr )
  data_df  = data_df.append( pd.Series( {'T' : T, 'dens.ave' : densi_ave, 'visco.ave' : visco_ave} ), ignore_index=True )

data_df.to_csv('transport.csv')
#fig = plt.figure()
#ax = fig.add_subplot(111)
#for m in m_list:
#  fix_df = visco_df.loc[ visco_df['m'] == m ]
#  if not fix_df.empty:
#    fix_df.plot( x='T', y='visco.ave', label=m, ax=ax)
#
#plt.show()
 


