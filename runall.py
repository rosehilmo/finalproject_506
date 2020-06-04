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

#ask user for the preferred temperature scale
temp_scale_dict = ['Kelvin', 'Celsius', 'Fahrenheit']
specify_scale = input ('Enter a number to specify the temperature scale. \nOptions: \n0 = Kelvin \n1 = Celsius \n2 = Fahrenheit \n')
# for some reason I couldn't get these working:
#if (specify_scale != 0) and (specify_scale != 1) and (specify_scale != 2):
	#specify_scale = 0
# if specify_scale not in range(0,2):
# 	specify_scale = 0
temp_scale = int(specify_scale)
print('You selected the ', temp_scale_dict[temp_scale], 'scale.')

filepath, filename = SST_functions.request_nc(lat_bounds,lon_bounds,time_bounds)

[dataset,time,time_label] =  SST_functions.read_nc(filepath,filename)

SST_functions.plot_SST(dataset,time,time_label,temp_scale,filepath)
