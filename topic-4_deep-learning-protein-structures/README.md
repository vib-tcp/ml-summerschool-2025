Link to the google colab search for github repos: https://colab.research.google.com/github/ 
with the repository: https://github.com/vib-tcp/ml-summerschool-2025/

- [Intro](https://docs.google.com/presentation/d/1rtVVJ-6dQNv9gAALjZJTg4HZxq7Onc2c03XFSwuUivQ/edit?usp=sharing)
- Schweke, Hugo, et al. "Discriminating physiological from non‐physiological interfaces in structures of protein complexes: a community‐wide study." [Proteomics 23.17 (2023): 2200323.](https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/10.1002/pmic.202200323)
- [PINDER](pinder.sh)


## Using the HPC
1. Go to tier1.hpc.ugent.be and log in
2. Request a Jupyter Notebook
  1. Cluster: dodrio gpu_rome_a100_80
  2. JupyterNotebook version: 7.0.2 GCCCore 12.3.0
  3. Working directory: `/dodrio/scratch/projects/2024_301/Deep-Learning-Protein-Structure-Prediction`
  4. Custom code:
     ```
     module load PyTorch-Geometric/2.5.0-foss-2023a-PyTorch-2.1.2-CUDA-12.1.1 Transformers/4.39.3-gfbf-2023a PyTorch-Lightning/2.2.1-foss-2023a-CUDA-12.1.1
export PATH="/dodrio/scratch/projects/2024_301/Deep-Learning-Protein-Structure-Prediction/pip_dir/dodrio/scratch/users/vsc49670/.local/:$PATH"
export PYTHONPATH=/dodrio/scratch/projects/2024_301/Deep-Learning-Protein-Structure-Prediction/pip_dir/dodrio/scratch/users/vsc49670/.local/lib/python3.11/site-packages/:$PYTHONPATH
     ```
  5. Reservation: vib_ml_summer_school_monday
  6. Launch
3. Make a folder for yourself with your name, only use this folder for your code and notebooks.
4. Make a new terminal, navigate to your folder and git clone this repo.

