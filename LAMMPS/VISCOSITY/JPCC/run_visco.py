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
 
scripts_dir = '/home/mdi0316/FUNCTIONS'
classes_dir = '/home/mdi0316/CLASSES'
sys.path.insert(0, scripts_dir)
sys.path.insert(0, classes_dir)

from Functions import print_tab, running_jobs, find_last_log
## read running jobs
run_ids, run_labels, run_status = running_jobs()

global work_dir
work_dir = os.getcwd()

input_file = os.path.join( work_dir,  'viscosity_CG.IL.in' )
cation_file = os.path.join( work_dir, 'cation_mol.txt' )
submit_file = os.path.join( work_dir, 'submit_lammps.sh' )
natoms_list = [50, 100, 500, 1000]
temp_list   = [200, 300, 400, 600]

def make_label(temp, nat):
    return  'JPCC.T.{}.nat.{}'.format(temp, nat)

def make_new_folder(temp, nat):
    new_fold = os.path.join( work_dir, 'RUNS', 'nat_{}'.format(nat), 'T_{}'.format(temp) )
    log_file = os.path.join( new_fold, 'log.lammps' )
    status = 'NEW'
    if os.path.exists( log_file ):
      log_lines = open( log_file, 'r' ).readlines()
      status = 'KO'
      if log_lines[-1].startswith('Total wall time'):
         status = 'OK'
    os.makedirs( new_fold, exist_ok=True )
    return status, new_fold

def main():

  old_lmp = open( input_file, 'r' ).readlines()
  data_df = pd.DataFrame(columns=['T', 'nat', 'status', 'dens.ave', 'visco.ave'])
  for nat in natoms_list:
    for temp in temp_list:
        tmp_label = make_label(temp, nat)
        if tmp_label in run_labels:
           status = 'RUN'
        else:
           status, new_fold = make_new_folder( temp, nat )
           if status == 'NEW':
              os.chdir( new_fold )
              shutil.copy2( submit_file, new_fold )
              shutil.copy2( cation_file, new_fold )
              os.chdir( new_fold )
              with open( 'viscosity_CG.IL.in', 'w+' ) as new_inp:
                for line in old_lmp:
                  if   line.startswith( 'create_atoms ' ):
                       new_line = line.replace('random 40', 'random {}'.format(nat) )
                  elif line    == 'variable    T equal 298\n':
                       new_line = 'variable    T equal {}\n'.format(temp)
                  else:
                     new_line = line
                  new_inp.write( new_line )
              sp.call( 'sbatch --partition=nodeshiq -J {} submit_lammps.sh viscosity_CG.IL.in '.format(tmp_label), shell = True )
 
        densi_file = os.path.join( new_fold, 'density.dat' )
        visco_file = os.path.join( new_fold, 'visco.dat' )
        densi_ave = float('nan')
        visco_ave = float('nan')
        if os.path.exists( densi_file ):
           densi_arr = np.array([ float(line.split()[2]) for line in open(densi_file, 'r').readlines()[1:] ])
           densi_ave = np.average( densi_arr )
        if os.path.exists( visco_file ):
           visco_arr = np.array([ float(line.split()[6]) for line in open(visco_file, 'r').readlines()[1:] ])
           visco_ave = np.average( visco_arr )
        data_df  = data_df.append( pd.Series( {'T' : temp, 'nat' : nat, 'status' : status, 'dens.ave' : densi_ave, 'visco.ave' : visco_ave} ), ignore_index=True )
  
  data_df.to_csv('transport.csv')

if __name__ == '__main__':
  main()
