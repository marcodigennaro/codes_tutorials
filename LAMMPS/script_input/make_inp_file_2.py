#!/home/mdi0316/anaconda3/bin/python

import numpy as np

lattice_parameter = 4.046 #Al in Ang

basis = np.array( [ [1.0, 0.0, 0.0], 
                    [0.0, 1.0, 0.0], 
                    [0.0, 0.0, 1.0], 
                   ] ) * lattice_parameter

base_atoms = np.array([ [0.0, 0.0, 0.0], 
                        [0.5, 0.5, 0.0], 
                        [0.5, 0.0, 0.5], 
                        [0.0, 0.5, 0.5]] ) * lattice_parameter 

system_size = 20

positions = []

for i in range(system_size):
  for j in range(system_size):
    for k in range(system_size):
      base_position = np.array([i,j,k])
      cartesian_position = np.inner( basis.T, base_position )
      for atom in base_atoms:
        positions.append( cartesian_position + atom )

with open( 'crys.data', 'w+' ) as fdata:
  fdata.write('# 2 lines ignored\n\n' )
  fdata.write('{} atoms\n'.format(len(positions)))
  fdata.write('{} atom types\n'.format(1))

  fdata.write('{} {} xlo xhi\n'.format(0, system_size*lattice_parameter ) )
  fdata.write('{} {} ylo yhi\n'.format(0, system_size*lattice_parameter ) )
  fdata.write('{} {} zlo zhi\n'.format(0, system_size*lattice_parameter ) )

  fdata.write('\n')

  fdata.write('Atoms\n\n')
  for i, pos in enumerate(positions):
    fdata.write( '{} 1 {} {} {}\n'.format(i+1, *pos) )

