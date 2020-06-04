"""
beginnings of the wrapper script

"""

############
# Grabing data from web
############

import SST_functions
#import xarray_troubleshoot

lat_bounds=[-20,20]  
lon_bounds=[-15,15]    
time_bounds=['2017-08-01T12:00:00Z','2017-08-10T12:00:00Z'] 

filepath, filename = SST_functions.request_nc(lat_bounds,lon_bounds,time_bounds)

[dataset,time,time_label] =  SST_functions.read_nc(filepath,filename)


