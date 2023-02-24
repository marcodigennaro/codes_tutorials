topo readlammpsdata solid.data
pbc box -center bb
set Ctions1 [atomselect top "type 4"]
set Ctions2 [atomselect top "type 2"]
set Ctails3 [atomselect top "type 3"]
set Anions [atomselect top "type 1"]
$Ctions1 set radius 4.0
$Ctions2 set radius 5.0
$Ctails3 set radius 5.0
$Anions set radius 10.0
