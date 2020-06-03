"""

Read in SST satellite data

"""
import numpy as np
import xarray as xr
import datetime
import matplotlib.pyplot as plt
import imageio
import os
import requests
import matplotlib.ticker as mticker
from netCDF4 import Dataset as netcdf_dataset
import datetime
#import pandas as pd
from pandas import DataFrame
import cmocean #need to install this first: pip install cmocean

from cartopy import config
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import request_nc

lat_bounds=[-20,20]  
lon_bounds=[-15,15]    
time_bounds=['2017-08-01T12:00:00Z','2017-08-20T12:00:00Z'] 
filepath, filename = request_nc.getSSTfiles(lat_bounds, lon_bounds, time_bounds)

#ask user for the preferred temperature scale
temp_scale_dict = ['Kelvin', 'Celsius', 'Fahrenheit']
specify_scale = input ('Enter a number to specify the temperature scale. \nOptions: \n0 = Kelvin \n1 = Celsius \n2 = Fahrenheit \n')
# for some reason I couldn't get these working:
# if (specify_scale != 0) and (specify_scale != 1) and (specify_scale != 2):
# 	specify_scale = 0
# if specify_scale not in range(0,2):
# 	specify_scale = 0
scale_selected = int(specify_scale)
print('You selected the ', temp_scale_dict[scale_selected], 'scale')

def nc_to_xr(filepath, filename):
	data_xr = xr.open_dataset(filepath + filename)
	# Data dimensions
	print('\n')
	print(data_xr.dims)

	# Data coordinates
	print('\n')
	print(data_xr.coords)

	# Data variables
	print('\n')
	print(data_xr.data_vars)

	# Extended information on variables
	# print(SST_xr.variables)
	
	return(data_xr)

data_xr = nc_to_xr(filepath, filename)

time = data_xr.variables['analysed_sst'][:,0,0]
time=len(time)
time=np.arange(time)
time=np.asarray(time)
print(time)

# time_label = data_xr.variables['time'][:] #Time is in epoch time, need to convert it to human readable time
# #Use datetime to convert to human readable:
# time_list = []
# for x in time:
#     lab = datetime.datetime.fromtimestamp(time_label[x]).strftime('%Y-%m-%d %H:%M:%S')
#     #print(lab)
#     time_list.append(lab)

# #Convert to data frame, separate date from time into different columns, keep date column only:
# time_label = DataFrame(time_list, columns=['date'])
# time_label['date'] = time_label['date'].str.split(r'\ ').str.get(0)

#preallocate
images = []
mov = 'movie.gif'

for x in time:
    plt.close('all') #clean up figures before proceding wiht next step of loop.
    #data:
    sst = data_xr.variables['analysed_sst'][x, :, :]
    lats = data_xr.variables['latitude'][:]
    lons = data_xr.variables['longitude'][:]

    if scale_selected == 0:
    	sst_plot = sst #keep Kelvin unites
    if scale_selected == 1:
    	sst_plot = sst-273.15 #convert Kelvin to Celsius
    if scale_selected == 2:
    	sst_plot = sst*(9/5) - 459.67 #convert Kelvin to Fahrenheit
    
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
    plot = plt.contourf(lons, lats, sst_plot, 60,transform=ccrs.PlateCarree(), cmap = cmap) #this plots the contourmap.

    #Title labels:
    title = 'Sea surface temperature (' + temp_scale_dict[scale_selected] + ') on ' #+ time_label['date'][x]
    plt.title(title, size = 12, fontweight = 'bold')

    #Legend:
    cbar = plt.colorbar(plot, orientation = 'vertical', pad = 0.1)
    #cbar.set_ticks([0,255])
    cbar.ax.tick_params(labelsize = 'small')
    cbar.set_clim(cmin,cmax)
    ax2 = cbar.ax
    ax2.text(4,0.35, 'Temperature (' + temp_scale_dict[scale_selected] + ')', rotation = 270, size = 10, fontweight = 'normal')

    #Saving plot:
    my_file= str(x) + '.png'
    plt.savefig(os.path.join(filepath, my_file))
    images.append(imageio.imread(os.path.join(filepath, my_file)))
    plt.show()

imageio.mimsave(os.path.join(filepath, mov), images)
