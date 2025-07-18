#!/bin/bash
#SBATCH --job-name=build-apptainer
#SBATCH --ntasks=1
#SBATCH --partition=debug_rome
#SBATCH --cpus-per-task=4
#SBATCH --gpus-per-node=1
#SBATCH --time=00:30:00
#SBATCH --output=build1_apptainer.stdout
#SBATCH --error=build1_apptainer.stderr
#SBATCH --account=2024_301
 
cd /tmp
chmod a+rwx .
cp $VSC_SCRATCH_PROJECTS_BASE/2024_301/<your subfolder>/containers/pycudadecon.def /tmp/pycudadecon.def
 
 
export APPTAINER_CACHEDIR=/tmp/.apptainer/cache
mkdir -p $APPTAINER_CACHEDIR
export APPTAINER_TMPDIR=/tmp/.apptainer/tmp
mkdir -p $APPTAINER_TMPDIR
apptainer build --nv pycudadecon.sif pycudadecon.def
 
mv /tmp/pycudadecon.sif $VSC_SCRATCH_PROJECTS_BASE/2024_301/<your subfolder>/containers/
