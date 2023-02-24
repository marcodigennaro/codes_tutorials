#!/bin/bash

#SBATCH --job-name=lammps_job_name
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=Marco.Di.Gennaro@external.toyota-europe.com
#SBATCH  -p nodeshiq 
#SBATCH --nodes=01
#SBATCH --ntasks-per-node=08
start_date=`date`
start_time="$(date -u +%s.%N)"
echo "Job slurm id: $SLURM_JOB_ID"
echo "Running on:   $SLURM_NODELIST"
echo "Running on:   $SLURM_NNODES nodes."
echo "Running on:   $SLURM_NPROCS processors."

#lammps=/home/mdi0316/anaconda3/bin/lmp_mpi
#lammps=/home/mdi0316/anaconda3/bin/lmp_serial
#lammps=/home/kgk6966/bin/lmp_mpi_cpu
lammps=/home/mdi0316/bin/lmp_mpi_src
#lammps=/home/mdi0316/bin/lmp_src

RUN_DIR="$PWD"
inp_file=$1
SLURM_TMPDIR="/tmp/mdi0316_slurm_$SLURM_JOB_ID"
echo "Remote  working directory is: $SLURM_TMPDIR"
echo "Current working directory is: $RUN_DIR"
echo "LAMMPS executable is: $lammps"
echo "Input file is: $inp_file"
echo "" 

###
mkdir $SLURM_TMPDIR
cd    $SLURM_TMPDIR
# copy all files to remote dir
for item in `ls $RUN_DIR`; do
  cp "${RUN_DIR}/${item}" .
  done

mpirun -np 08 $lammps < $inp_file > lmps_out.$SLURM_JOB_ID

# copy all files back to run dir
for item in `ls $SLURM_TMPDIR`; do
  cp "${SLURM_TMPDIR}/${item}" ${RUN_DIR}
  done
## 

end_date=`date`
end_time="$(date -u +%s.%N)"
elapsed="$(bc <<<"$end_time-$start_time")"
echo "Starting at: $start_date"
echo "Ending at:   $end_date"

echo "Total of $elapsed seconds elapsed for process"

