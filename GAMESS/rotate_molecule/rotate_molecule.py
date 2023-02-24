#!/home/mdi0316/anaconda3/bin/python

import os, re, sys
import pandas as pd
import subprocess as sp
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import numpy as np

scripts_dir = '/home/mdi0316/FUNCTIONS'
classes_dir = '/home/mdi0316/CLASSES'
sys.path.insert(0, scripts_dir)
sys.path.insert(0, classes_dir)

from sklearn.cluster import KMeans

from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

from datetime import datetime
now = datetime.now()
month = now.strftime("%B")

desktop_work_dir='/home/mdi0316/WORK_Desktop/{}'.format(month[:3].upper())

from mendeleev import element
from numpy import linalg as LA
from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm

import ast

from Functions  import *
from Plot       import *

## PRINT one example

run_dir = '/data/mdi0316/WORK/DIMERS/C1MIM_BF4/RUNS/SCAN_from_ISOLATED/N311/B3LYP/T_5/P_0/R_4.0/OPT/DFT'
bead_coords_csv = os.path.join( run_dir, 'beads_coords.csv' )
acac_csv = os.path.join( run_dir, 'atomic_coords_and_charges.csv' )

bead_coords_df = pd.read_csv( bead_coords_csv , index_col = 0 )
acac_df  = pd.read_csv( acac_csv , index_col = 0 )

for k,v in dict(acac_df['acac']).items():
    acac_dict = ast.literal_eval(v)

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

cart_coords = np.array( [ [cc['x'],cc['y'],cc['z']] for cc in acac_dict.values() if cc['elem.'] != 'H' ] ).astype(float)
ax.scatter( cart_coords[:,0], cart_coords[:,1], cart_coords[:,2], 'k', s=100 )

## rotate matrix
cart_coords = rotate_molecule(cart_coords)
ax.scatter( cart_coords[:,0], cart_coords[:,1], cart_coords[:,2], 'r', s=100 )


X,Y = np.linspace(-5,5,100),np.linspace(-5,5,100)
X, Y = np.meshgrid(X, Y)
Z = np.zeros_like(X)
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10, color='g', alpha=0.1)
ax.plot_wireframe(X, Z, Y, rstride=10, cstride=10, color='g', alpha=0.1)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
