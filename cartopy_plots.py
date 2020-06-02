"""
Plots netCDF sea surface temperature for eaxh timeopint and generates a .gif movie for the whole time series.

"""
#################
# IMPORTS:
#################

import imageio
import os
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import datetime
#import pandas as pd
from pandas import DataFrame

from cartopy import config
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#################
#open and read the dataset, save an iterable range of times
    #note to zinka: time iterable is fricken stupid as it stands
#################

#create filepath to save png files to
filepath='PNG_files/'
if os.path.isdir(filepath) == False:
    os.mkdir(filepath)

dataset = netcdf_dataset('noaacwBLENDEDsstDaily_8423_ee32_0effevan.nc')
time = dataset.variables['analysed_sst'][:,0,0]
time=len(time)
time=np.arange(time)
time=np.asarray(time)
print(time)

#################
# Getting date labels to put in the images:
#################
time_label = dataset.variables['time'][:] #Time is in epoch time, need to convert it to human readable time
#Use datetime to convert to human readable:
time_list = []
for x in time:
    lab = datetime.datetime.fromtimestamp(time_label[x]).strftime('%Y-%m-%d %H:%M:%S')
    #print(lab)
    time_list.append(lab)

#Convert to data frame, separate date from time into different columns, keep date column only:
time_label = DataFrame(time_list, columns=['date'])
time_label['date'] = time_label['date'].str.split(r'\ ').str.get(0)

#################
# plotting
#################

#preallocate
images = []
mov = 'movie.gif'

time = [0,1] #temporary, just for testing

#save png slides to the filepath
for x in time:
    #data:
    sst = dataset.variables['analysed_sst'][x, :, :]
    lats = dataset.variables['latitude'][:]
    lons = dataset.variables['longitude'][:]

    #This code plots on the Plate Caree maps
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    #latitude/longitude labels and lines (This can be modified based on what people like)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylables_top = False
    gl.xlines = True
    gl.ylines = True
    #gl.xlocator = mticker.FixedLocator([-180,-45,0,45,180]) #Right now, lat/long lines are absolute, need to make them relative for our data!
    gl.xfprmater = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    #gl.xlabel_style = {'size': 6, 'color': 'gray'} #formating of lables
    #gl.xlabel_style = {'color': 'red', 'weight': 'bold'} #more formating of labels

    #plotting data:
    plot = plt.contourf(lons, lats, sst, 60,transform=ccrs.PlateCarree()) #this plots the contourmap.

    #Title labels:
    title = 'Sea surface temperature (K) on ' + time_label['date'][x]
    plt.title(title, size = 12, fontweight = 'bold')

    #Legend: NEEDS TO BE FIXED, right now its doing weird things inside the loop, i get multiple legends... 
    cbar = plt.colorbar(plot, ax=ax)
    cbar.set_label('Temperature (K)', rotation = 270)

    #Saving plot:
    my_file= str(x) + '.png'
    plt.savefig(os.path.join(filepath, my_file))
    images.append(imageio.imread(os.path.join(filepath, my_file)))

imageio.mimsave(os.path.join(filepath, mov), images)
#Alternative way to make gif*but requires ImageMagic, which might not be worrth it.
#convert -delay 45 -loop 0 *.png movie2.gif #lets you sepcify how fast you want the images to switch.


####################
#things to fix:
####################
    #time iteration make it nicer
    #add labels to graph... have the date displayed on each image --> DONE
    #Add title to image --> DONE
    #Ad scalebar to image
    #Add if statements for missing data
    #What units is temperature in? K or C?
