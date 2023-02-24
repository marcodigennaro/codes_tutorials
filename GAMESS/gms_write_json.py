#!/home/mdi0316/anaconda3/bin/python

### common input start
import os, sys, re
import numpy as np
import pandas as pd
import shutil
import subprocess as sp
import datetime
import time
import math

scripts_dir = '/home/mdi0316/FUNCTIONS'
classes_dir = '/home/mdi0316/CLASSES'
zmat_converter_dir = '/home/mdi0316/CLASSES/zmatrix-master'
sys.path.insert(0, scripts_dir)
sys.path.insert(0, classes_dir)
sys.path.insert(0, zmat_converter_dir)

import GAMESS
import json
from Functions import running_jobs
run_ids, run_job_labels = running_jobs()

def recursive_items(dictionary, depth):
    depth += 1
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value, depth)
        else:
            yield ('Depth: {}'.format( depth ), key, value)

def read_input( filename ):
    inp_lines = open( filename, 'r' ).readlines()
    inp_dict = {}
    for count, line in enumerate(inp_lines):
        if line.strip().startswith('$'):
           tmp_card = line.replace('$','').strip()
           if not tmp_card == 'END':
              inp_dict[tmp_card] = {}
        else:
           if '=' in line:
              tmp_k, tmp_v = line.split('=')
              inp_dict[tmp_card][tmp_k.strip()] = tmp_v.strip()
           else:
              inp_dict['DATA'][count] = line.split() 
    return( inp_dict ) 

def main():

  run_dir = os.getcwd()
  obj_inp = sys.argv[1]
  inp_dict = read_input( obj_inp )
  
  tmp_coords = inp_dict['CONTRL']['COORD'] 
  tmp_runtyp = inp_dict['CONTRL']['RUNTYP']

  if 'MPLEVL' in inp_dict['CONTRL'].keys():
     tmp_postscf = 'MP2'
     tmp_postscf_lab = 'MP2'
     mp2 = True
     dft = False
     optimize = False
  elif 'DFTTYP' in inp_dict['CONTRL'].keys():
     tmp_postscf = 'DFTTYP'
     tmp_postscf_lab = 'DFT'
     dft = True
     mp2 = False
     optimize = True
  else:
     tmp_postscf = 'NONE'
     tmp_postscf_lab = 'NONE'

  if tmp_coords == 'UNIQUE':
     natoms = len(inp_dict['DATA']) - 2
  elif tmp_coords == 'ZMT':
     natoms = int( (6.+float( inp_dict['CONTRL']['NZVAR'] ))/3 )

  obj_calc = GAMESS.GAMESS( inp_name = obj_inp, run_dir = run_dir, natoms = natoms, 
                            run_type = tmp_runtyp, post_scf = tmp_postscf, coordinates = tmp_coords )


  calc_exec, calc_exec_err = obj_calc.get_job_exec()
  print( '\n === Calculation {}, Error {} === \n'.format(calc_exec, calc_exec_err))
  calc_out_dict = obj_calc.get_out_dict()

  if calc_exec == 'TERMINATED.NORMALLY':
    print( 'All keys in dict: {}'.format( calc_out_dict.keys()) )
    for k,v in calc_out_dict.items():
        if k in [ 'ZMAT', 'INTERNUCL.DISTANCES', 'MULL.CHARGES' ]:
           pass
        else:
          if isinstance(v, dict):
             print( '   all keys in {}: {}'.format( k, v.keys() ) )
          else:
             print( k, v )

    with open( 'gms.json', 'w+' ) as json_file:
         json.dump( calc_out_dict, json_file )
  else:
    calc_err = obj_calc.read_error()
    print( '\n === Calculation FAILED: {} === \n'.format(calc_err) )
  

  print( calc_out_dict.keys() )
  if tmp_coords == 'ZMT' and tmp_runtyp == 'OPTIMIZE':
     print_zmat = input('Print zmat? (Y)')
     if print_zmat == 'Y':
        lowest_conf = obj_calc.get_lowest_opt_energy()
        for k,v in lowest_conf.items():
            print(k,v)
        
  if optimize:
    print_ccc = input('Print cart_coords.csv? (Y)')
    if print_ccc == 'Y':
       cart_df = pd.DataFrame(columns = [ 'Radius', 'cart.coords.', 'mull.charges' ] ) 
       cart_coords = calc_out_dict['FINAL']['CART.COORDS.']
       mull_charges = calc_out_dict['MULL.CHARGES'] 

       cart_dict = { 'Radius' : '1', 'cart.coords.' : cart_coords, 'mull.charges' : mull_charges }
       cart_series = pd.Series( cart_dict, dtype=object )
       cart_df = cart_df.append( cart_series , ignore_index=True )

       cart_df.to_csv( 'cart_coords.csv' )
 

if __name__ == '__main__':
  main()

