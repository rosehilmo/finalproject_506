"""
beginnings of the wrapper script

"""

############
# Grabing data from web
############

import request_nc
<<<<<<< HEAD
import xarray_troubleshoot
=======
import xarray
>>>>>>> 14f3c56f11545ebcf03b749dc1f818bff429716f

lat_bounds = [80,85]
lon_bounds = [45,90]
time_bounds = ['2017-08-01T12:00:00Z', '2017-08-03T12:00:00Z']

<<<<<<< HEAD
filepath, filename = request_nc.getSSTfiles(lat_bounds,lon_bounds,time_bounds)
=======
[filepath,filename]=request_nc.getSSTfiles(lat_bounds,lon_bounds,time_bounds)

sst_xarray=xarray.open_dataset(filepath + filename,engine='scipy',decode_times=False)

>>>>>>> 14f3c56f11545ebcf03b749dc1f818bff429716f
