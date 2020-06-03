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
import cmocean #need to install this first: pip install cmocean

from cartopy import config
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import request_nc

#################
#open and read the dataset, save an iterable range of times
    #note to zinka: time iterable is fricken stupid as it stands
#################

lat_bounds=[-20,20]
lon_bounds=[-15,15]
time_bounds=['2017-08-01T12:00:00Z','2017-08-20T12:00:00Z']

[filepathSST,filenameSST]=request_nc.getSSTfiles(lat_bounds,lon_bounds,time_bounds)

#create filepath to save png files to
filepath='PNG_files/'
if os.path.isdir(filepath) == False:
    os.mkdir(filepath)

dataset = netcdf_dataset(filepathSST+filenameSST,"r",format="NETCDF3_64BIT_DATA")
time = dataset.variables['analysed_sst'][:,0,0]
time=len(time)
time=np.arange(time)
time=np.asarray(time)
print(time)

#################
# Getting min and max absolute sst for entire dataset:
#################



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

#time = [0,1] #temporary, just for testing small number of images

#save png slides to the filepath
for x in time:
    plt.close('all') #clean up figures before proceding wiht next step of loop.
    #data:
    sst = dataset.variables['analysed_sst'][x, :, :]
    lats = dataset.variables['latitude'][:]
    lons = dataset.variables['longitude'][:]

    #This code plots on the Plate Caree maps
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    #latitude/longitude labels and lines (This can be modified based on what people like)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
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
    #vmin = 280 #setting minimim and meximum temperatures that will be plotted (in K)
    #vmax = 310
    cmap = cmocean.cm.thermal #setting colormap
    #plot = plt.contourf(lons, lats, sst, 60,transform=ccrs.PlateCarree(), vmin = vmin, vmax = vmax, colormap = cmap)
    plot = plt.contourf(lons, lats, sst, 60,transform=ccrs.PlateCarree(), cmap = cmap) #this plots the contourmap.

    #Title labels:
    title = 'Sea surface temperature (K) on ' + time_label['date'][x]
    plt.title(title, size = 12, fontweight = 'bold')

    #Legend:
    cbar = plt.colorbar(plot, orientation = 'vertical', pad = 0.1)
    #plt.clim(min_temp, max_temp)
    cbar.ax.tick_params(labelsize = 'small')
    ax2 = cbar.ax
    ax2.text(4,0.35, 'Temperature (K)', rotation = 270, size = 10, fontweight = 'normal')

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
    #Ad scalebar to image --> legend needs to be fixed... so that the legend scale is the same across all images?
    #Add if statements for missing data
    #What units is temperature in? K or C?
    #Colormap selection? --> redblue cmap from cmocean --> DONE
    #thinner linewidth on the lat/lon grid --> DONE
    #
