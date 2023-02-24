dimension 3
boundary f f f
atom_style full
units metal			## ev, ang
dielectric 2.0			##
bond_style harmonic
angle_style harmonic

neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes

## GEOMETRY
region box1 block -40.0 40.0 -40.0 40.0 -40.0 40.0
create_box 4 box1 bond/types 2 extra/bond/per/atom 2 angle/types 1 extra/angle/per/atom 1  ## num particles types etc...

mass    1  290.0 #anion ie bf4 
mass    2  130.0 #ring
mass    3  130.0 #methyl
mass    4  130.0 #ethyl

create_atoms 1 single  10.0 0.0 0.0
create_atoms 2 single   0.0 0.0 0.0               #!!! Position of central particle (eg. ring)
create_atoms 3 single   0.0 5.0 0.0               #!!! Position of "side chain" 1
create_atoms 4 single   0.0 -3.535534 3.535534    #!!! Position of "side chain" 1
group anion type 1
group ring type 2
group methyl type 3
group ethyl type 4

bond_coeff 1 200.0 5.0                   #!!! bond spring constant and equilibrium length [A] (length should be equal to the bond distance as defined above)
bond_coeff 2 200.0 5.0                   #!!! bond
angle_coeff 1 200.0 135.0                #!!! angle

## DUMMY INTERACTION
## we define this before creating bonds
pair_style lj/cut 30.0
pair_modify mix geometric
################### properties to optimise with EASY
pair_coeff 1 1   0.0013009 10.0 30.0      #!!!eps [eV] sigma [A] cutoff (=3*sigma) [A]
pair_coeff 2 2   0.0013009  5.0 15.0
pair_coeff 3 3   0.0013009  5.0 15.0
pair_coeff 4 4   0.0013009  5.0 15.0

create_bonds single/bond 1 2 3    # bond type1 btw p2 and p3
create_bonds single/bond 2 2 4    # bond type2 btw p2 and p4
create_bonds single/angle 1 3 2 4 # angle type1 btw p2, p3 and p4


kspace_style msm 1.0e-6
kspace_modify pressure/scalar yes
set type 2 charge  1.0
set type 1 charge -1.0

## REAL INTERACTION
## after bonds are created
pair_style lj/cut/coul/msm 30.0
pair_modify mix geometric
################### properties to optimise with EASY  (Just repeat the lines from above)
pair_coeff 1 1   0.0013009 10.0 30.0
pair_coeff 2 2   0.0013009  5.0 15.0
pair_coeff 3 3   0.0013009  5.0 15.0
pair_coeff 4 4   0.0013009  5.0 15.0

########################################


thermo_style	custom step temp pe ke ebond press density
thermo       100

#write_data solid.data pair ij

#variable  ILdens equal density
variable  anx equal x[1]
variable  any equal y[1]
variable  anz equal z[1]
variable  ILdist equal sqrt(x[1]*x[1]+y[1]*y[1]+z[1]*z[1])   #!!!Distance from the origin (should correcpond to the N position from EMIM)
variable  ILtemp equal temp
variable  ILpe equal pe
variable  ILke equal ke
variable  ILpr equal press

##################################
velocity  all zero linear
reset_timestep  0
fix	  333 all print 1 "${ILdist} ${theta} ${phi} ${anx} ${any} ${anz} ${ILpe}" file density.dat screen no 
#dump 1 all dcd 1 minim.dcd

variable  dist   equal  4.0   #!!!minimum radius for radial scanning [Angstrom]
timestep	.1            # !!! dt per step (Velocity is 1.0)
##################################
#  Loop for angles
##################################
label theta_loop
variable j loop 0 18
variable theta equal $j*10

label phi_loop
variable k loop 0 36
variable phi equal $k*10

variable  vxx equal sin($(v_theta/180*PI))*cos($(v_phi/180*PI))
variable  vyy equal sin($(v_theta/180*PI))*sin($(v_phi/180*PI))
variable  vzz equal cos($(v_theta/180*PI))
variable  xx equal v_dist*v_vxx
variable  yy equal v_dist*v_vyy
variable  zz equal v_dist*v_vzz

set atom 1 x ${xx} y ${yy} z ${zz}
fix      1 anion move linear ${vxx} ${vyy} ${vzz}

run             350       #!!! Number of steps (Use 1 for fixed radius)
#run             1

next k
jump in.CG.IL phi_loop
next j
jump in.CG.IL theta_loop

##################################

#write_data solid4.data pair ij    #!!!Uncomment if you need the final geometry

