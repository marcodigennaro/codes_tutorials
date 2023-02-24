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
from Functions import *

GMS = GAMESS.GAMESS( inp_name = 'gms_SCAN_from_ISOLATED_c1mim_bf4_T_5_P_270_R_10.0_N311_B3LYP_OPT_DFT.inp',
                     run_dir = './' , natoms = 24, 
                     run_type = 'RUN', post_scf = 'OPTIMIZE' )

print(GMS)
print(dir(GMS))
