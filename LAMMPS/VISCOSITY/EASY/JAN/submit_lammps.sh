#!/bin/bash

#SBATCH --job-name=lammps_job_name
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=Marco.Di.Gennaro@external.toyota-europe.com
#SBATCH  -p nodesloq 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
echo "Job slurm id: $SLURM_JOB_ID"
echo "Starting at:  `date`"
echo "Running on:   $SLURM_NODELIST"
echo "Running on:   $SLURM_NNODES nodes."
echo "Running on:   $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

#lammps=/home/mdi0316/anaconda3/bin/lmp_mpi
#lammps=/home/mdi0316/anaconda3/bin/lmp_serial
#lammps=/home/kgk6966/bin/lmp_mpi_cpu
lammps=/home/mdi0316/bin/lmp_src

RUN_DIR="$PWD"
inp_file=$1

SLURM_TMPDIR="/tmp/mdi0316_slurm_$SLURM_JOB_ID"
mkdir $SLURM_TMPDIR
cd $SLURM_TMPDIR

echo "Remote  working directory is `pwd`"

cp $RUN_DIR/* $SLURM_TMPDIR

$lammps < viscosity_CG.IL.in 

mv $SLURM_TMPDIR/* $RUN_DIR

echo "Ending at:  `date`"

