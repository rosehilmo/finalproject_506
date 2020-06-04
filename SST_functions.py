

import os
import requests
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import datetime
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import cmocean

from cartopy import config
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import imageio

def request_nc(lat_bounds,lon_bounds,time_bounds):

    """
    Gets global daily SST satellite data 2002-present
    with 5km resolution in netCDF format from
    https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsstDaily.html
    :param tuple lat_bounds: Latitudes bounding region of interest
    :param tuple lon_bounds: Longitudes bounding region of interest
    :param tuple time_bounds: Times bounding days of interest in format 2017-08-01T12:00:00Z
    :return tuple: string of filepath and filename for downloaded files
    """

    print('Beginning file download with requests')
    website="https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsstDaily.nc?"
    lat_rq='[('+ str(min(lat_bounds)) + '):1:(' + str(max(lat_bounds)) + ')]'
    lon_rq='[('+ str(min(lon_bounds)) + '):1:(' + str(max(lon_bounds)) + ')]'
    time_rq='[(' + time_bounds[0] + '):1:(' + time_bounds[1] + ')]'
    rq=time_rq+lat_rq+lon_rq

    sst_url=website + "analysed_sst" + rq + ",analysis_error" + rq + ",mask" + rq + ",sea_ice_fraction" + rq
    r = requests.get(sst_url)
    if r.status_code == 404:
        return ['Request failed: No data in time period or wrong request format']
    filename='noaacwBLENDEDsstDaily' + time_bounds[0][0:10]  + '_' + time_bounds[1][0:10]  +'.nc'
    filepath='SST_files/'
    if os.path.isdir(filepath) == False:
        os.mkdir(filepath)
    with open(filepath + filename, 'wb') as f:
        f.write(r.content)
        return [filepath,filename]


def read_nc(filepath,filename):
    """
    Read satellite nc file

    :param string filepath: path to file
    :param string filename: name of file

    :return netcdf dataset: Array of sst over time and space
    :return list: Time indices
    :return list: Time labels

    """

    dataset = netcdf_dataset(filepath+filename,"r",format="NETCDF3_64BIT_DATA")
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

    return [dataset,time,time_label]


def plot_SST(dataset,time,time_label,temp_scale,filepath):

    """
    Make daily plots of SST in region and produce gif.

    :param netcdf dataset: sst dataset producted by read_nc
    :param list time: time indices from read_nc
    :param list time_label: List of time strings
    :param int temp_scale: integer specifying F, C or Kelvin
    :param string filepath: output folder to save figures to
    """
    #################
    # plotting
    #################

    #preallocate
    images = []

    if os.path.isdir(filepath)  == False:
        os.mkdir(filepath)

    #time = [0,1] #temporary, just for testing small number of images

    #save png slides to the filepath
    max_k=np.max(dataset.variables['analysed_sst'][:,:,:])
    min_k=np.min(dataset.variables['analysed_sst'][:,:,:])

    if temp_scale == 2: #=='Fahrenheit'
        cmax=max_k * (9/5) - 459.67
        cmin=min_k * (9/5) - 459.67
    if temp_scale == 1: #== 'Celsius'
        cmax=max_k - 273.15
        cmin=min_k - 273.15
    if temp_scale == 0: #== 'Kelvin'
        cmax=max_k
        cmin=min_k


    for x in time:
        plt.close('all') #clean up figures before proceding wiht next step of loop.
        #data:
        sst = dataset.variables['analysed_sst'][x, :, :]
        lats = dataset.variables['latitude'][:]
        lons = dataset.variables['longitude'][:]

    #specify temperature scale
        temp_scale_dict = ['Kelvin', 'Celsius', 'Fahrenheit']
        if temp_scale == 0: #=='Kelvin'
            sst_plot=sst
        if temp_scale == 2: # =='Fahrenheit'
            sst_plot=np.subtract(np.multiply(sst,9/5),459.67)
        if temp_scale == 1: #=='Celsius'
            sst_plot=np.subtract(sst,273.15)

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
        gl.xfprmater = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        #plotting data:
        cmap = cmocean.cm.thermal #setting colormap
        plot = plt.contourf(lons, lats, sst_plot, 60,transform=ccrs.PlateCarree(), cmap = cmap) #this plots the contourmap.

        #Title labels:
        title = 'Sea surface temperature (' + temp_scale_dict[temp_scale] + ') on ' + time_label['date'][x]
        plt.title(title, size = 12, fontweight = 'bold')

        #Legend:
        cbar = plt.colorbar(plot, orientation = 'vertical', pad = 0.1)
        plot.set_clim(cmin,cmax)
        ax2 = cbar.ax
        ax2.text(4,0.35, 'Temperature (' + temp_scale_dict[temp_scale] + ')', rotation = 270, size = 10, fontweight = 'normal')

        #Saving plot:
        my_file= str(x) + '.png'
        plt.savefig(os.path.join(filepath, my_file))
        images.append(imageio.imread(os.path.join(filepath, my_file)))
        #plt.show()

    movie_file = 'movie.gif'
    imageio.mimsave(os.path.join(filepath, movie_file), images)

    return()
