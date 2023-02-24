#!/bin/bash

#SBATCH --job-name=job_name
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=Marco.Di.Gennaro@external.toyota-europe.com
#SBATCH -p nodeshiq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16

start_date=`date`
start_time="$(date -u +%s.%N)"
echo "Job slurm id: $SLURM_JOB_ID"
echo "Running on:   $SLURM_NODELIST"
echo "Running on:   $SLURM_NNODES nodes."
echo "Running on:   $SLURM_NPROCS processors."

job_label=`echo $1 | sed "s/.nw//g"`
log_file="log.${job_label}_$SLURM_JOB_ID"
nwchem=/home/mid0316/CODES/nwchem-6.8.1/bin/LINUX64/nwchem
nwchem=/home/kgk6966/src/nwchem/nwchem-6.8.1/bin/LINUX64/nwchem

export LOCALDIR=/data/scratch-no-backup/mdi0316/runnwchem
export LDIR=$LOCALDIR/$SLURM_JOBID

echo "Current working directory is: $SLURM_SUBMIT_DIR"
echo "Rungms local dir is: $LDIR"
echo "Input file is: $1"
echo "Log   file is: $log_file"
echo "which nwchem:  $nwchem"

mkdir -p $LDIR/tmp
#cd $LDIR

cp $SLURM_SUBMIT_DIR/*.inp .


mpirun -np 16 $nwchem $1 >& $log_file 2> err.gms
#rungms_local ${job_label}.inp 00 16 >& $log_file

mv $LDIR/tmp/*.dat $SLURM_SUBMIT_DIR/
rm -fR $LDIR/tmp
cp -r $LDIR/* $SLURM_SUBMIT_DIR/
rm -fR $LDIR


end_date=`date`
end_time="$(date -u +%s.%N)"
elapsed="$(bc <<<"$end_time-$start_time")"
echo "Starting at: $start_date"
echo "Ending at:   $end_date"

echo "Total of $elapsed seconds elapsed for process"

