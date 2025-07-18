#!/bin/bash 
#SBATCH --account=2024_301
#SBATCH --chdir=/dodrio/scratch/projects/2024_301/<your subfolder>/mcmicro
#SBATCH --partition=cpu_rome
#SBATCH --nodes=1
#SBATCH --job-name=mcmicro_github
#SBATCH --gpus-per-node=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=mcmicro_githubc.out
#SBATCH --error=mcmicro_githubc.err
 
export APPTAINER_CACHEDIR=/dodrio/scratch/projects/024_301/<your subfolder>/.apptainer_cachedir
export APPTAINER_TMPDIR=/dodrio/scratch/projects/024_301/<your subfolder>/.apptainer_tmpdir
module load Nextflow
nextflow run labsyspharm/mcmicro --in exemplar-001 -profile singularity  -with-report raport_ugentconfig
