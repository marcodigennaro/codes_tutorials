#!/home/mdi0316/anaconda3/bin/python

import numpy as np

natoms = 1000

system_size = 20.0

positions = []

for i in range(natoms):
  positions.append( np.random.rand(3)*system_size )

with open( 'rand.data', 'w+' ) as fdata:
  fdata.write('# 2 lines ignored\n\n' )
  fdata.write('{} atoms\n'.format(natoms))
  fdata.write('{} atom types\n'.format(1))

  fdata.write('{} {} xlo xhi\n'.format(0, system_size ) )
  fdata.write('{} {} ylo yhi\n'.format(0, system_size ) )
  fdata.write('{} {} zlo zhi\n'.format(0, system_size ) )

  fdata.write('\n')

  fdata.write('Atoms\n\n')
  for i, pos in enumerate(positions):
    fdata.write( '{} 1 {} {} {}\n'.format(i+1, *pos) )

