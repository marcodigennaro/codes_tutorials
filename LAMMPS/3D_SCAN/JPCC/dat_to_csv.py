#!/home/mdi0316/anaconda3/bin/python

import pandas as pd

coords_cols = [('Coordinates','Radius'), ('Coordinates','Theta'), ('Coordinates','Phi')]
result_cols = [('Results','Int.En.')]
pot_file = 'pot_ener.dat'
csv_file = 'pot_ener.csv'
df_file  = pd.DataFrame( columns=pd.MultiIndex.from_tuples(coords_cols+result_cols) )

pot_lines = open( pot_file, 'r' ).readlines()
for pot_line in pot_lines[1:]:
  rr, tt, pp, ee = [ float(item) for item in pot_line.split() ]
  df_file = df_file.append( pd.Series( {('Coordinates','Radius') : rr, 
                                        ('Coordinates','Theta')  : tt, 
                                        ('Coordinates','Phi')    : pp, 
                                        ('Results','Int.En.')    : ee }
                                      ), ignore_index=True )

print(df_file)
df_file.to_csv( csv_file )

