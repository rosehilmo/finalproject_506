# finalproject_506
Final project for Zinka, Mary Margaret, Evan, and Rose for OCEAN506. Downloads sea surface temperature (SST) satellite data as .nc files for regions and times of your choice from 2002-present. Then daily SST maps are plotted and saved as .png files, and finally combined as a .gif movie.

## Instructions for setup:
Clone git repository in your home directory.

Setup environment and get essential packages with these commands:
 
conda env create --quiet --file environment.yml

conda activate finalproject_506

When done using this environment, use command: conda deactivate

## To run code in python:
runall.py is a wrapper file that combines all the components of the code.
Open runall.py in any code editor and define your latitude, longitude, and time parameters then save the file.
Run runall.py. It will request text input for whether you want Celcius, Farenheit, or Kelvin.
Code may take several minutes to run if more than 1 month of global temperature data is requested.


