import os, shutil
import numpy as np
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from giscube.config import MEDIA_ROOT, MEDIA_URL
from scripts.extract_shp_table import extract_shp_table
from scripts.netcdf_info import get_nc_data
from scripts.conversion import nc_to_gtif
from netCDF4 import Dataset

@dajaxice_register(method='GET')
def remove_loaded_file(request, param):
    Uploaded_file = MEDIA_ROOT + MEDIA_URL + param
    os.remove(Uploaded_file)
    #and remove the associated folder for a file is exists
    try:
        shutil.rmtree('{0}'.format(Uploaded_file[:-4]))
    except:
        pass
    
    
@dajaxice_register(method='GET')
def reproject_vector(request, selected_vector, selected_proj, vector_name):
    s = 'ogr2ogr -f "ESRI Shapefile" -s_srs EPSG:27700 -t_srs EPSG:4326 {0} {1}'.format(MEDIA_ROOT+MEDIA_URL+vector_name, MEDIA_ROOT+MEDIA_URL+selected_vector+'.shp')
    os.system(s)


@dajaxice_register(method='GET')
def extract_shp_table_text(request, selected_vector, text_name):
    print MEDIA_ROOT+MEDIA_URL+selected_vector
    print MEDIA_ROOT+MEDIA_URL+text_name
    extract_shp_table(MEDIA_ROOT+MEDIA_URL+selected_vector+'.shp', MEDIA_ROOT+MEDIA_URL+text_name)
    

@dajaxice_register(method='GET')
def get_netcdf_times(request, nc_file, time_var):
    print ">>>> Getting netCDF times"
    nc_dataset = Dataset(MEDIA_ROOT+MEDIA_URL+nc_file, mode='r')
    time_data = nc_dataset.variables[time_var][:]
    times = [float(t) for t in time_data]
    print ">>>> Getting netCDF times (Done)"
    print ">>> List of time: {0}".format(times)
    return simplejson.dumps({'time_data': times}) 

@dajaxice_register(method='GET')
def map_netcdf(request, nc_file, latitude_var, longitude_var, time_var, value_var, selected_time):
    print ">>>> Mapping netCDF data"
    nc_dataset = Dataset(MEDIA_ROOT+MEDIA_URL+nc_file, mode='r')
    latitude_data = nc_dataset.variables[latitude_var][:]
    longitude_data = nc_dataset.variables[longitude_var][:]
    time_data = nc_dataset.variables[time_var][:]
    selected_time_index = np.where(time_data==float(selected_time))[0][0]
    value_data = get_nc_data(nc_file, latitude_var, longitude_var, time_var, value_var, selected_time_index)
    nc_to_gtif(latitude_data, longitude_data, value_data)
    print ">>>> Mapping netCDF data (Done)"
    print values.shape
    