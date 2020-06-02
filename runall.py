"""
beginnings of the wrapper script

"""

############
# Grabing data from web
############

import request_nc
import xarray

lat_bounds = [80,85]
lon_bounds = [45,90]
time_bounds = ['2017-08-01T12:00:00Z', '2017-08-03T12:00:00Z']

[filepath,filename]=request_nc.getSSTfiles(lat_bounds,lon_bounds,time_bounds)

sst_xarray=xarray.open_dataset(filepath + filename,engine='scipy',decode_times=False)

