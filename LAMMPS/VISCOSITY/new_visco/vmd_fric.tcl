topo readlammpsdata solid5.data
pbc box -center bb
set Ctions [atomselect top "type 1"]
set Ctails [atomselect top "type 2"]
set Anions [atomselect top "type 3"]
$Ctions set radius 5.0
$Ctails set radius 5.0
$Anions set radius 10.0
