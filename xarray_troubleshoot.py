"""

Read in SST satellite data

"""
import numpy as np
import xarray as xr

# filepath, filename = rq_nc.getSSTfiles(lat_bounds, lon_bounds, time_bounds)

def nc_to_xr(filepath):
	data_xr = xr.open_dataset(filepath)
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

path_in='/Users/MMStoll/Python/Data/EffectiveComputing_Data/NOAA_SST_Daily.nc'
path_in1='/Users/MMStoll/Python/Data/EffectiveComputing_Data/testSST.nc'

data_xr = nc_to_xr(path_in)
data_xr1 = nc_to_xr(path_in1)
