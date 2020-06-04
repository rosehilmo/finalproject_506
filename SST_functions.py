

import os
import requests
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import datetime
from pandas import DataFrame 



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