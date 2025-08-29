Connecting the SODA kernel to an Ondemand Jupyter Lab session.


SSH to the node that your Code Server is running.   
`ssh nodeXXXX`  


Then, in your home folder make a symlink to the Spatial summerschool folder:  
`ln -s /dodrio/scratch/projects/2024_301/Spatial-Omics-Data-Analysis summer_spatial`  

CD to the project forlder with the symlink:  
`cd summer_spatial`  

Load conda  
`module load Miniconda3/23.5.2-0`  

In a terminal activate our Environment  
`conda activate .miniconda3/envs/SODA`  


#Add the kernel to the jupyer notebook  
`python -m ipykernel install --user --name SODA --display-name "Python (SODA)"`  

Now in your ondemand requested Jupyter lab you should be able to select the SODA kernel  
