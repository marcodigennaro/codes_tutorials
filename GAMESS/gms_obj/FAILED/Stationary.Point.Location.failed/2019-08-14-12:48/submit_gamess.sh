#!/bin/bash

#SBATCH --job-name=gms_SCAN_from_ISOLATED_c1mim_bf4_T_5_P_270_R_10.0_N311_B3LYP_OPT_DFT.inp
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=Marco.Di.Gennaro@external.toyota-europe.com
#SBATCH -p nodesloq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
##SBATCH --exclude=node001,node002,node003,node004

start_date=`date`
start_time="$(date -u +%s.%N)"
echo "Job slurm id: $SLURM_JOB_ID"
echo "Running on:   $SLURM_NODELIST"
echo "Running on:   $SLURM_NNODES nodes."
echo "Running on:   $SLURM_NPROCS processors."

job_label=`echo $1 | sed "s/.inp//g"`
log_file="log.${job_label}_$SLURM_JOB_ID"

export LOCALDIR=/data/scratch-no-backup/mdi0316/rungms
export LDIR=$LOCALDIR/$SLURM_JOBID

echo "Current working directory is: $SLURM_SUBMIT_DIR"
echo "Rungms local dir is: $LDIR"
echo "Input file is: $1"
echo "Log   file is: $log_file"
echo "which rungms: `which rungms`"

mkdir -p $LDIR/tmp
#cd $LDIR

cp $SLURM_SUBMIT_DIR/*.inp .

rungms_scratch ${job_label}.inp 00 16 >& $log_file 2> err.gms
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

