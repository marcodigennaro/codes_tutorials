#!/home/mdi0316/anaconda3/bin/python

import os, sys,re
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import scipy.constants as const
Ha2eV =  const.value('hartree-electron volt relationship')

remote_dir='/data/scratch-no-backup/mdi0316/WORK'

fix_18_csv=os.path.join( remote_dir, 'EMIM_BF4_fix_18', 'N311', 'CSV', 'scan_out.csv' )
fix_3_csv =os.path.join( remote_dir, 'EMIM_BF4_fix_3',  'N311', 'CSV', 'scan_out.csv' )

fix_18_pd = pd.read_csv( fix_18_csv, index_col=0 )
fix_3_pd  = pd.read_csv( fix_3_csv, index_col=0 )

fix_t = 90
fix_p = 0

reduced_18 = fix_18_pd.loc[ fix_18_pd['Theta'] == fix_t ].loc[ fix_18_pd['Phi'] == fix_p ]
reduced_3  = fix_3_pd.loc[ fix_3_pd['Theta'] == fix_t ].loc[ fix_3_pd['Phi'] == fix_p ]
reduced_18['Int.Ener.'] = Ha2eV*reduced_18['Int.Ener.']
reduced_3[ 'Int.Ener.'] = Ha2eV*reduced_3[ 'Int.Ener.']

def dat_to_csv( lmps_data ):
  lmps_lines = open(lmps_data, 'r').readlines()
  with open( lmps_data, 'w+' ) as new_lmps:
    for line in lmps_lines:
      new_line = line
      if line.startswith( '#' ):
        new_line = ',Radius,Theta,Phi,Int.Ener.\n'
      new_lmps.write( '{}'.format(new_line) ) 

min_csv = 'null_ener.csv'
no_min  = 'minimize_ener.csv'
#lmps_data = sys.argv[1]
#dat_to_csv( lmps_data )
dat_to_csv( min_csv )
dat_to_csv( no_min  )
min_df = pd.read_csv( min_csv, index_col=0 )
no_min_df = pd.read_csv( no_min, index_col=0 )

fig = plt.figure()
ax  = fig.add_subplot(111)
reduced_18.plot(x='Radius', y='Int.Ener.', ax=ax, label='18')
reduced_3.plot( x='Radius', y='Int.Ener.', ax=ax, label='3')
min_df.plot(   x='Radius', y='Int.Ener.', ax=ax, label='lmps.minimize')
no_min_df.plot(   x='Radius', y='Int.Ener.', ax=ax, label='lmps.no_min')
plt.show()
plt.close()

