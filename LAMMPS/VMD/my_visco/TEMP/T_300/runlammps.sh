#!/bin/bash
# Spread the tasks evenly among the nodes
# Want the node exlusively
#SBATCH --time=24:00:00
#SBATCH --job-name=100_visc
#SBATCH -p nodeshiq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

#module add mvapich2/gcc

#mpirun lmp_mpi_cpu -in viscosity_CG.IL.in

mpirun ~/anaconda3/bin/lmp_serial -in viscosity_CG.IL.in
