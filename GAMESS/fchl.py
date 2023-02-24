#!/home/mdi0316/anaconda3/bin/python

### common input start
import os, sys, re
import numpy as np
import pandas as pd
import shutil
import subprocess as sp
import datetime

import getpass
user = getpass.getuser()

scripts_dir = '/home/mdi0316/FUNCTIONS'
classes_dir = '/home/mdi0316/CLASSES'
sys.path.insert(0, scripts_dir)
sys.path.insert(0, classes_dir)

import IONIC_LIQUID as IL
import GAMESS
from Regression import pred_GPR_3D, pred_KRR, get_dataset
from Functions  import *

import json

from qml.fchl import generate_representation
calc = GAMESS.GAMESS( inp_file = 'gms_bf4_N21_PBE0_OPT_DFT.inp', run_dir = './', run_type = 'OPTIMIZE', post_scf = 'DFTTYP', natoms = 5 )

scan_exec, scan_inp_dict, scan_out_dict, scan_err, scan_scf, scan_geom = calc.get_job_results()

cart_coords  = scan_out_dict['FINAL']['CART.COORDS.']
mull_charges = scan_out_dict['FINAL']['MULL.CHARGES']

bf4_coord = np.empty([0,3])

for kk, tmp_dict in cart_coords.items():
    x = float(tmp_dict['x']) 
    y = float(tmp_dict['y']) 
    z = float(tmp_dict['z'])
    bf4_coord = np.vstack( ( bf4_coord, [x,y,z] ) )

bf4_charg = np.array([float(v['charge']) for v in mull_charges.values() ])

print(bf4_coord.shape)
print(bf4_charg.shape)
rep = generate_representation(bf4_coord, bf4_charg)
#print(rep)
#
import ast
#csv_file = '/data/mdi0316/WORK/DIMERS/EMIM_BF4/CSV/N21/M11/cart_coords.csv'
csv_file = 'cart_coords.csv'
df = pd.read_csv(csv_file, index_col = 0, dtype=object)

for idx, row in df.iterrows():
    cart_coords = ast.literal_eval(row['cart.coords.'])
    mull_charges = ast.literal_eval(row['mull.charges'])
    
    at_charg = np.array([float(v['charge']) for v in mull_charges.values() ])
    at_coord = np.empty([0,3])
    for kk, tmp_dict in cart_coords.items():
        x = float(tmp_dict['x']) 
        y = float(tmp_dict['y']) 
        z = float(tmp_dict['z'])
        print( kk, tmp_dict, [x,y,z] )
        at_coord = np.vstack( ( at_coord, [x,y,z] ) )
        rep = generate_representation( at_coord, at_charg[0:int(kk)+1] )
        print( kk, at_coord, len(at_charg[0:int(kk)+1]) )
    
    print( at_coord.shape ) 
    print( at_charg.shape ) 
    rep = generate_representation( at_coord, at_charg )
    print(rep)
