dimension 3
boundary f f f
atom_style full
units metal
dielectric 2.0
bond_style harmonic
angle_style harmonic

neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes

region box1 block -40.0 40.0 -40.0 40.0 -40.0 40.0
create_box 4 box1 bond/types 2 extra/bond/per/atom 2 angle/types 1 extra/angle/per/atom 1

#molecule cat_ion cation_mol.txt
mass    1  290.0 #anion
mass    2  67.0 #ring
mass    3  15.0 #methyl
mass    4  29.0 #ethyl

create_atoms 1 single  10.0 0.0 0.0
create_atoms 2 single   0.930064 0.67314 0.003587
create_atoms 3 single   3.618873 0.602433 0.01098
create_atoms 4 single   -1.57953 -0.87466 0.74759
group anion type 1
group ring type 2
group methyl type 3
group ethyl type 4

bond_coeff 1 200.0 2.689748837
bond_coeff 2 200.0 3.04931147
angle_coeff 1 200.0 144.1868904
pair_style lj/cut 30.0
pair_modify mix geometric
################### properties to change
pair_coeff 1 1   0.0013009 10.0 30.0
pair_coeff 2 2   0.0013009  5.0 15.0
pair_coeff 3 3   0.0013009  5.0 15.0
pair_coeff 4 4   0.0013009  5.0 15.0
#create_bonds ring methyl 1 1.0 10.0
#create_bonds ring ethyl  1 1.0 10.0

create_bonds single/bond 1 2 3
create_bonds single/bond 2 2 4
create_bonds single/angle 1 3 2 4


kspace_style msm 1.0e-6
kspace_modify pressure/scalar yes
set type 1 charge -1.0
set type 2 charge  0.408675
set type 3 charge  0.317505 
set type 4 charge  0.273820

pair_style lj/cut/coul/msm 30.0
pair_modify mix geometric
################### properties to change
pair_coeff 1 1   0.0013009 10.0 30.0
pair_coeff 2 2   0.0013009  5.0 15.0
pair_coeff 3 3   0.0013009  5.0 15.0
pair_coeff 4 4   0.0013009  5.0 15.0

########################################


thermo_style	custom step temp pe ke ebond press density
thermo       100

write_data solid.data pair ij

variable  dist   equal  3.8   #minimum scanning radius
#variable  ILdens equal density
variable  anx equal x[1]
variable  any equal y[1]
variable  anz equal z[1]
variable  ILdist equal sqrt(x[1]*x[1]+y[1]*y[1]+z[1]*z[1])
variable  ILstep equal step
#variable  ILtime equal time/1000000 #from fs to ns
variable  ILtemp equal temp
variable  ILpe equal pe
variable  ILke equal ke
variable  ILpr equal press

##################################
velocity  all zero linear
reset_timestep  0
timestep	2.0
fix	  333 all print 1 "${ILdist} ${theta} ${phi} ${anx} ${any} ${anz} ${ILpe}" file density.dat screen no 
#dump 1 all dcd 1 minim.dcd

##################################
#  Loop for angles
##################################
fix frzanion anion setforce 0.0 0.0 0.0
fix frzring  ring  setforce 0.0 0.0 0.0
label theta_loop
variable j loop 0 18
#variable j loop 0 0
variable theta equal $j*10

label phi_loop
variable k loop 0 36
#variable k loop 0 0
variable phi equal $k*10

variable  vxx equal sin($(v_theta/180*PI))*cos($(v_phi/180*PI))
variable  vzz equal sin($(v_theta/180*PI))*sin($(v_phi/180*PI))
variable  vyy equal cos($(v_theta/180*PI))
#variable  vxx equal sin($(v_theta/180*PI))*cos($(v_phi/180*PI))
#variable  vyy equal sin($(v_theta/180*PI))*sin($(v_phi/180*PI))
#variable  vzz equal cos($(v_theta/180*PI))
variable  xx equal v_dist*v_vxx
variable  yy equal v_dist*v_vyy
variable  zz equal v_dist*v_vzz

set atom 1 x ${xx} y ${yy} z ${zz}
fix      1 anion move linear ${vxx} ${vyy} ${vzz}
run             10
#minimize 1.e-4 1.0e-6 100 1000
#run             1

next k
jump in.CG.IL phi_loop
next j
jump in.CG.IL theta_loop

##################################

#write_data solid4.data pair ij

