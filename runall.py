"""
Wrapper script where variables are defined and functions are called.

Codes get global daily SST satellite data 2002-present with 5km resolution in netCDF format from
https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsstDaily.html
and plots daily .pngs, combining them into a .gif
"""

import SST_functions
import cmocean

###########PARAMETERS########

lat_bounds=[-20,20]  
lon_bounds=[-15,15]    
time_bounds=['2017-08-01T12:00:00Z','2017-08-10T12:00:00Z'] 

colormap = cmocean.cm.thermal # Check this link for other colormap options https://matplotlib.org/cmocean/

############################
#####END OF PARAMETERS######
############################

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

SST_functions.plot_SST(dataset,time,time_label,temp_scale,'Figures/',cmap = colormap)
