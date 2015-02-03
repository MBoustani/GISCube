import os, shutil
import numpy as np
import json
from netCDF4 import Dataset
from dajaxice.decorators import dajaxice_register
from giscube.config import MEDIA_ROOT, MEDIA_URL

from scripts.extract_shp_table import extract_shp_table
from scripts.metadata import get_nc_data
from scripts.conversion import nc_to_gtif, nc_to_geojson, shp_to_kml, convert_geotiff_to_kml, shp_to_tif, shp_to_json
from scripts.clip_geotiff_by_shp import clip_geotiff_by_shp
from scripts.data_management import change_geotiff_resolution
from scripts.opendap import load as load_opendap
from scripts.opendap import opendap_metadata


@dajaxice_register(method='GET')
def opendap_getdata(request, opendap_url, opendap_variable):
    text_file = load_opendap(opendap_url, opendap_variable)
    return json.dumps({'status': '<div class="alert alert-success" role="alert" >Successfully retrieved data. Please refresh the page.</div>'})


@dajaxice_register(method='GET')
def opendap_getmetadata(request, opendap_url):
    metadata = opendap_metadata(opendap_url)
    return json.dumps({'metadata': metadata.splitlines()})


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
def reproject_shapefile(request, selected_shapefile, shapefile_re_project_epsg, projected_shapefile_name):
    if projected_shapefile_name.split(".")[-1] != "shp":
        projected_shapefile_name = "{0}.shp".format(projected_shapefile_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, projected_shapefile_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        s = 'ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:{2} {0} {1}'.format(MEDIA_ROOT+MEDIA_URL+projected_shapefile_name, MEDIA_ROOT+MEDIA_URL+selected_shapefile+'.shp', shapefile_re_project_epsg)
        os.system(s)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def reproject_geotiff(request, selected_geotiff, geotif_re_project_epsg, projected_geotiff_name):
    if projected_geotiff_name.split(".")[-1] != "tif" or projected_geotiff_name.split(".")[-1] != "tiff":
        projected_geotiff_name = "{0}.tif".format(projected_geotiff_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, projected_geotiff_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        s = "gdalwarp -t_srs 'epsg:{2}' {0} {1}".format(MEDIA_ROOT+MEDIA_URL+selected_geotiff, MEDIA_ROOT+MEDIA_URL+projected_geotiff_name, geotif_re_project_epsg)
        os.system(s)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def extract_shp_table_text(request, selected_vector, text_name):
    if text_name.split(".")[-1] != "txt":
        text_name = "{0}.txt".format(text_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, text_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        extract_shp_table(MEDIA_ROOT+MEDIA_URL+selected_vector+'.shp', MEDIA_ROOT+MEDIA_URL+text_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def extract_netcdf_header(request, selected_netcdf, text_name):
    if text_name.split(".")[-1] != "txt":
        text_name = "{0}.txt".format(text_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, text_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        s = "ncdump -h {0} > {1}".format(MEDIA_ROOT+MEDIA_URL+selected_netcdf, MEDIA_ROOT+MEDIA_URL+text_name)
        os.system(s)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def dump_netcdf_to_text(request, selected_netcdf, text_name):
    if text_name.split(".")[-1] != "txt":
        text_name = "{0}.txt".format(text_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, text_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        s = "ncdump {0} > {1}".format(MEDIA_ROOT+MEDIA_URL+selected_netcdf, MEDIA_ROOT+MEDIA_URL+text_name)
        os.system(s)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def get_netcdf_times(request, nc_file, time_var):
    nc_dataset = Dataset(MEDIA_ROOT+MEDIA_URL+nc_file, mode='r')
    time_data = nc_dataset.variables[time_var][:]
    times = [float(t) for t in time_data]
    return json.dumps({'time_data': times})


@dajaxice_register(method='GET')
def netcdf_to_geotiff(request, nc_file, latitude, longitude, time, value, selected_time, geotiff_name):
    if geotiff_name.split(".")[-1] != "tif" or geotiff_name.split(".")[-1] != "tiff":
        geotiff_name = "{0}.tif".format(geotiff_name)
    nc_dataset = Dataset(MEDIA_ROOT+MEDIA_URL+nc_file, mode='r')
    latitude_data = nc_dataset.variables[latitude][:]
    longitude_data = nc_dataset.variables[longitude][:]
    time_data = nc_dataset.variables[time][:]
    selected_time_index = np.where(time_data==float(selected_time))[0][0]
    value_data = get_nc_data(nc_file, latitude, longitude, time, value, selected_time_index)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, geotiff_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        nc_to_gtif(latitude_data, longitude_data, value_data, geotiff_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def netcdf_to_geojson(request, nc_file, latitude, longitude, time, value, selected_time, geojson_name):
    if geojson_name.split(".")[-1] != "json":
        geojson_name = "{0}.json".format(geojson_name)
    nc_dataset = Dataset(MEDIA_ROOT+MEDIA_URL+nc_file, mode='r')
    latitude_data = nc_dataset.variables[latitude][:]
    longitude_data = nc_dataset.variables[longitude][:]
    time_data = nc_dataset.variables[time][:]
    selected_time_index = np.where(time_data==float(selected_time))[0][0]
    value_data = get_nc_data(nc_file, latitude, longitude, time, value, selected_time_index)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, geojson_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        nc_to_geojson(latitude_data, longitude_data, value_data, geojson_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def shapefile_to_kml(request, selected_shp, kml_name):
    if kml_name.split(".")[-1] != "kml":
        kml_name = "{0}.kml".format(kml_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, kml_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        shp_to_kml(MEDIA_ROOT + MEDIA_URL + selected_shp + '.shp', MEDIA_ROOT + MEDIA_URL + kml_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def shapefile_to_tif(request, selected_shp, tif_name, shp_to_tif_layer, shp_to_tif_epsg, shp_to_tif_width, shp_to_tif_height, shp_to_tif_ot, shp_to_tif_burn1, shp_to_tif_burn2, shp_to_tif_burn3):
    if tif_name.split(".")[-1] != "tif" or tif_name.split(".")[-1] != "tiff":
        tif_name = "{0}.tif".format(tif_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, tif_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        shp_to_tif(selected_shp, tif_name, shp_to_tif_layer, shp_to_tif_epsg, shp_to_tif_width, shp_to_tif_height, shp_to_tif_ot, shp_to_tif_burn1, shp_to_tif_burn2, shp_to_tif_burn3)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def shapefile_to_json(request, selected_shp, shp_to_json_file, shp_to_json_epsg):
    if shp_to_json_file.split(".")[-1] != "json":
        shp_to_json_file = "{0}.json".format(shp_to_json_file)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, shp_to_json_file)):
        return json.dumps({'status': 'File already exists.'})
    else:
        shp_to_json(selected_shp, shp_to_json_file, shp_to_json_epsg)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def clip_geotiff_by_shapefile(request, selected_geotiff, selected_shapefile, clipped_geotiff_name):
    if clipped_geotiff_name.split(".")[-1] != "tif" or clipped_geotiff_name.split(".")[-1] != "tiff":
        clipped_geotiff_name = "{0}.tif".format(clipped_geotiff_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, clipped_geotiff_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        clip_geotiff_by_shp(MEDIA_ROOT + MEDIA_URL + selected_geotiff , MEDIA_ROOT + MEDIA_URL + selected_shapefile + '.shp', MEDIA_ROOT + MEDIA_URL + clipped_geotiff_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def geotiff_to_kml(request, selected_geotiff, geotiff_to_kml_name):
    if geotiff_to_kml_name.split(".")[-1] != "kml":
        geotiff_to_kml_name = "{0}.kml".format(geotiff_to_kml_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, geotiff_to_kml_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        convert_geotiff_to_kml(selected_geotiff, geotiff_to_kml_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def geotiff_resolution(request, selected_geotiff, geotiff_new_x_res, geotiff_new_y_res, geotiff_new_resolution_name):
    if geotiff_new_resolution_name.split(".")[-1] != "tif" or geotiff_new_resolution_name.split(".")[-1] != "tiff":
        geotiff_new_resolution_name = "{0}.tif".format(geotiff_new_resolution_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, geotiff_new_resolution_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        change_geotiff_resolution(selected_geotiff, geotiff_new_x_res, geotiff_new_y_res, geotiff_new_resolution_name)
        return json.dumps({'status': 'Done'})

