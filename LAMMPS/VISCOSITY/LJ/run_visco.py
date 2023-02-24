#!/home/mdi0316/anaconda3/bin/python

import os, re, sys
import random
from random import randint
from itertools import cycle
import shutil
import math 
import subprocess as sp
 
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

def make_label(temp, tmp_exp, nat):
    return  'LJ.T.{}.step.{}.nat.{}'.format(temp, tmp_exp, nat)

def make_new_folder(temp, tmp_exp, nat):
    new_fold = os.path.join( work_dir, 'RUNS', 'timestep_{}'.format(tmp_exp), 'nat_{}'.format(nat), 'T_{}'.format(temp) )
    os.makedirs( new_fold, exist_ok=True )
    return new_fold

def main():

  old_lmp = open( input_file, 'r' ).readlines()
  for tmp_exp in [0, 2, 4, 6]:
    for nat in [20, 40, 80]:
      for temp in [200, 400, 600]:
        tmp_label = make_label(temp, tmp_exp, nat)
        if tmp_label in run_labels:
           pass
        else:
           new_fold = make_new_folder( temp, tmp_exp, nat )
           os.chdir( new_fold )
           shutil.copy2( submit_file, new_fold )
           shutil.copy2( cation_file, new_fold )
           os.chdir( new_fold )
           with open( 'viscosity_CG.IL.in', 'w+' ) as new_inp:
             for line in old_lmp:
               if   line.startswith( 'create_atoms ' ):
                    new_line = line.replace('random 40', 'random {}'.format(nat) )
               elif line    == 'variable    T equal 300\n':
                    new_line = 'variable    T equal {}\n'.format(temp)
               elif line    == 'variable    dt equal 4.0\n':
                    new_line = 'variable    dt equal 1e-{}\n'.format(tmp_exp)
               else:
                  new_line = line
               new_inp.write( new_line )
           sp.call( 'sbatch --partition=nodeshiq -J {} submit_lammps.sh'.format(tmp_label), shell = True )
  
if __name__ == '__main__':
  main()
