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

from LAMMPS import LAMMPS_CALC
from Functions import print_tab, running_jobs, find_last_log
## read running jobs
run_ids, run_labels, run_status = running_jobs()

work_dir = os.getcwd()

all_dir = [ item for item in os.listdir(work_dir) if os.path.isdir(item) and item != '__pycache__' ]
print(all_dir)

cation_file = os.path.join( work_dir, 'cation_mol.txt' )
submit_file = os.path.join( work_dir, 'submit_lammps.sh' )
nat_list = [100] #, 500, 1000]
t_list   = [300] #, 400, 500, 600]

def main():
  data_df = pd.DataFrame(columns=['type', 'n_atoms', 'T', 'status', 'error', 'dens.ave', 'visco.ave'])
  for tmp_dir in all_dir:
    interaction = tmp_dir.replace('OPT_','').split('_')[:-1]
    if interaction == ['FULL']:
       input_file = os.path.join( work_dir,  'FULL_viscosity_CG.IL.in' )
    elif interaction == ['NON', 'COUL']:
       input_file = os.path.join( work_dir,  'NON_COUL_viscosity_CG.IL.in' )
    os.chdir(os.path.join(work_dir,tmp_dir))

    param_file = os.path.join( work_dir, tmp_dir, 'best_task', 'task.dat' )
    params = [ float(item) for item in  open( param_file, 'r' ).readlines() ]
    e11, e22, e33, e44, s11, s22, s33, s44, n_exp, m_exp = params[1:]
    
    e12, s12 = math.sqrt( e11 * e22 ), math.sqrt( s11 * s22 )
    e13, s13 = math.sqrt( e11 * e33 ), math.sqrt( s11 * s33 )
    e14, s14 = math.sqrt( e11 * e44 ), math.sqrt( s11 * s44 )
    e23, s23 = math.sqrt( e22 * e33 ), math.sqrt( s22 * s33 )
    e24, s24 = math.sqrt( e22 * e44 ), math.sqrt( s22 * s44 )
    e34, s34 = math.sqrt( e33 * e44 ), math.sqrt( s33 * s44 )
    
    for n_at in nat_list:
      for temp in t_list:
         status = None
         tmp_label = 'T.{}.{}at.{}'.format(temp, n_at, tmp_dir)
         densi_ave = float('nan')
         visco_ave = float('nan')
         run_dir = os.path.join( work_dir, tmp_dir, '{}_at'.format(n_at), 'T_{}'.format(temp) )
         LMPS = LAMMPS_CALC( run_dir, tmp_label )
         if tmp_label in run_labels:
            status = 'running'
         else:
            if os.path.exists( run_dir ):
               if os.path.exists( LMPS.log_file ):
                  status, error = LMPS.read_lammps_log()
                  if status == 'completed':
                     input_file = os.path.join( run_dir, 'viscosity_CG.IL.in' )
                     densi_file = os.path.join( run_dir, 'density.dat' )
                     visco_file = os.path.join( run_dir, 'visco.dat' )
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
            else:
              status = 'NEW'
              os.makedirs( run_dir )
              shutil.copy2( submit_file, run_dir )
              shutil.copy2( cation_file, run_dir )
              os.chdir( run_dir )
              old_lmp = open( input_file, 'r' ).readlines()
              with open( 'viscosity_CG.IL.in', 'w+' ) as new_inp:
                for line in old_lmp:
                  if line.startswith( 'variable    T equal' ):
                     new_line = 'variable    T equal {}\n'.format(temp) 
                  elif line.startswith('create_atoms 0 random 20'):
                     new_line = 'create_atoms 0 random {} 2345 box1 mol cat_ion 1234\n'.format(n_at) 
                  elif line.startswith('create_atoms 1 random 20'):
                     new_line = 'create_atoms 1 random {} 1340 box1\n'.format(n_at)
                  elif line.startswith('velocity     all create'):
                     new_line = 'velocity     all create $T 987654321 mom yes rot yes dist gaussian\n'
                  elif line.startswith( 'pair_coeff 1 1' ):
                     new_line = 'pair_coeff 1 1 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e11, s11, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 1 2' ):
                     new_line = 'pair_coeff 1 2 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e12, s12, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 1 3' ):
                     new_line = 'pair_coeff 1 3 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e13, s13, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 1 4' ):
                     new_line = 'pair_coeff 1 4 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e14, s14, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 2 2' ):
                     new_line = 'pair_coeff 2 2 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e22, s22, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 2 3' ):
                     new_line = 'pair_coeff 2 3 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e23, s23, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 2 4' ):
                     new_line = 'pair_coeff 2 4 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e24, s24, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 3 3' ):
                     new_line = 'pair_coeff 3 3 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e33, s33, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 3 4' ):
                     new_line = 'pair_coeff 3 4 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e34, s34, n_exp, m_exp ) 
                  elif line.startswith( 'pair_coeff 4 4' ):
                     new_line = 'pair_coeff 4 4 {:4.8f} {:4.8f} {} {:4.4f}\n'.format( e44, s44, n_exp, m_exp ) 
                  else:
                     new_line = line
                  new_inp.write( new_line )
              sp.call( 'sbatch --partition=nodeshiq -J {} submit_lammps.sh'.format(tmp_label), shell = True )

         data_df  = data_df.append( pd.Series( { 'type' : tmp_dir,  'n_atoms' : n_at, 'T' : temp, 
                                                 'status' : status, 'error' : error, 
                                                 'dens.ave' : densi_ave, 'visco.ave' : visco_ave} ), ignore_index=True )
  

  data_df.to_csv( os.path.join( work_dir, 'all_transport.csv' ))




if __name__ == '__main__':
  main()
