#!/bin/bash
#SBATCH -A 2024_301
#SBATCH --partition=gpu_rome_a100_40
#SBATCH --nodes="1"
#SBATCH --ntasks-per-node="1"
#SBATCH --cpus-per-task=16
#SBATCH --gpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=output_careamics_nalan.out
#SBATCH --error=error_careamics_nalan.err
#SBATCH --time=02:00:00
source activate careamics
python /dodrio/scratch/projects/2024_301/<your subfolder>/containers/test_nalan_careamics.py
