import sys

try:
    from osgeo import gdal
    from osgeo import osr
except ImportError:
    import gdal
    import osr
try:
    from osgeo import ogr
except ImportError:
    import ogr

from netCDF4 import Dataset
import numpy as np
import urllib2
import json

def get_nc_data(nc_file, latitude_var, longitude_var, time_var, value_var, selected_time_index):
    print nc_file
    nc_dataset = open_file(nc_file)
    if nc_dataset:
        lat = nc_dataset.variables[latitude_var]
        lon = nc_dataset.variables[longitude_var]
        time = nc_dataset.variables[time_var]
        value = nc_dataset.variables[value_var]
        
        lat_dim = lat.dimensions
        lon_dim = lon.dimensions
        time_dim = time.dimensions
        value_dim = value.dimensions

        lat_shape = lat.shape
        lon_shape = lon.shape
        time_shape = time.shape
        value_shape = value.shape

        print 'Latitude shape: {0}'.format(lat_shape)
        print 'Longitude shape: {0}'.format(lon_shape)
        print 'Time shape: {0}'.format(time_shape)
        print 'Value shape: {0}'.format(value_shape)

        print "Getting dimensions info"
        dims_info = {}
        for i, each in enumerate(lat_dim):
            dims_info[each] = lat_shape[i]

        for i, each in enumerate(lon_dim):
            dims_info[each] = lon_shape[i]

        for i, each in enumerate(time_dim):
            dims_info[each] = time_shape[i]

        print "Slicing vlaues"
        slices = ()
        for dim in value_dim:
            if dim in dims_info:
                if dim in time_dim:
                    slices += (slice(selected_time_index,selected_time_index+1),)
                else:
                    slices += (slice(0,dims_info[dim]+1),)
            else:
                slices += (slice(0,1),)
        print "Values sliced"
        print np.squeeze(value[slices]).shape
        return np.squeeze(value[slices])

def open_file(file_path):
    try:
        nc_file = Dataset(file_path, mode='r')
        if not nc_file:
            raise "File cannot be opened"
        return nc_file
    except:
        raise "File cannot be opened"
        sys.exit()

def get_variables(nc_file):
    if nc_file:
        return [variable.encode() for variable in nc_file.variables.keys()]


def get_file_name(file_path):
    if file_path:
        return file_path


def variables_info(nc_file, all_variables):
    variables_info = []
    for value in all_variables:
        variable = nc_file.variables[value]
        each_variable = {}
        each_variable[value] = {}
        each_variable[value]['dimensions'] = variable.dimensions
        for att in variable.ncattrs():
            each_variable[value][att] = variable.getncattr(att)
        variables_info.append(each_variable)

    return variables_info


def get_nc_metadata(file_path):
    try:
        nc_metadata = urllib2.urlopen("http://127.0.0.1:18080/uploaded_files/{0}/?output=json&traverse".format(file_path)).read()
        dic = json.loads(nc_metadata)
        nc_variables = []
        for each in dic['leaves']:
            nc_variables.append(each['name'])
        return {'file_name':file_path, 'nc_metadata':nc_metadata, 'nc_variables':nc_variables}
    except:
        return None


def get_hdf_metadata(file_path):
    try:
        hdf_metadata = urllib2.urlopen("http://127.0.0.1:18080/uploaded_files/{0}/?output=json&traverse".format(file_path)).read()
        return {'file_name':file_path, 'hdf_metadata':hdf_metadata}
    except:
        return None

#####shp_name_info.py

def open_shp_file(file_path):
    try:
        vector_file = ogr.Open(file_path)
        if not vector_file:
            raise "File cannot be opened"
        return vector_file
    except:
        raise "File cannot be opened"
        sys.exit()

def get_shp_name(vector_file):
    try:
        file_name = vector_file.GetName()
        return file_name
    except:
        return None

def get_shp_format(vector_file):
    try:
        file_format = vector_file.GetDriver().GetName()
        return file_format
    except:
        return None

def get_shp_number_of_layers(vector_file):
    try:
        number_of_layers = vector_file.GetLayerCount()
        return number_of_layers
    except:
        return None

def get_shp_layer(vector_file, layer_index):
    try:
        layer = vector_file.GetLayerByIndex(layer_index)
        return layer
    except:
        return None

def get_shp_layer_name(layer_file):
    try:
        layer_name = layer_file.GetName()
        return layer_name
    except:
        return None

def get_shp_number_of_feature(layer_file):
    try:
        number_of_feature = layer_file.GetFeatureCount()
        return number_of_feature 
    except:
        return None

def get_shp_layer_type(layer_file):
    try:
        geom_type_index = layer_file.GetLayerDefn().GetGeomType()
        layer_type = ogr.GeometryTypeToName(geom_type_index)
        return layer_type
    except:
        return None

def get_shp_layer_spatial_reference(layer_file):
    try:
        layer_spatial_reference = layer_file.GetSpatialRef().ExportToPrettyWkt()
        return layer_spatial_reference
    except:
        return None

def get_shp_layer_extend(layer_file):
    try:
        layer_extend = layer_file.GetExtent()
        return layer_extend
    except:
        return None


def run_shp_info(file_path):
    layers = []
    vector_file = open_shp_file(file_path)     #To open vector file
    file_name = get_shp_name(vector_file)     #To print file name
    file_format = get_shp_format(vector_file)     #To print file format
    file_number_of_layers = get_shp_number_of_layers(vector_file)     #To print number of layer/s
    for layer_index in range(file_number_of_layers):
        layer = {}
        layer_file = get_shp_layer(vector_file, layer_index)
        layer['layer file'] = layer_file
        layer_name = get_shp_layer_name(layer_file)
        layer['layer name'] = layer_name
        number_of_feature = get_shp_number_of_feature(layer_file)
        layer['number of feature'] = number_of_feature
        layer_type = get_shp_layer_type(layer_file)
        layer['layer type'] = layer_type
        layer_spatial_reference = get_shp_layer_spatial_reference(layer_file)
        layer['layer spatial reference'] = layer_spatial_reference
        layer_extend = get_shp_layer_extend(layer_file)
        layer['layer extend'] = layer_extend
        layers.append(layer)
    
    return {'file_name':file_name, 'file_format':file_format , 'num_layer':str(file_number_of_layers),\
            'layer_name':layer['layer name'], 'number_of_feature':layer['number of feature'],\
    'layer_type':layer['layer type'], 'layer_spatial_reference':layer['layer spatial reference'],\
    'layer_extend':layer['layer extend']}



#####tif_name_info.py

def open_tif(file_path):
    try:
        raster_file = gdal.Open(file_path)
        if not raster_file:
            raise "File cannot be opened"
        return raster_file
    except:
        raise "File cannot be opened"
        sys.exit()

def get_tif_name(raster_file):
    try:
        file_name = raster_file.GetDescription()
        return file_name
    except:
        return None

def get_tif_format(raster_file):
    try:
        file_format = raster_file.GetDriver().LongName
        return file_format
    except:
        return None

def get_raster_number_of_band(raster_file):
    try:
        raster_number_of_band = raster_file.RasterCount
        return raster_number_of_band
    except:
        return None

def get_raster_x_y_size(raster_file):
    try:
        raster_x_y_size = [raster_file.RasterXSize, raster_file.RasterYSize]
        return raster_x_y_size
    except:
        return None

def get_raster_projection(raster_file):
    try:
        raster_projection = raster_file.GetProjectionRef()
        hSRS = osr.SpatialReference()
        hSRS.ImportFromWkt(raster_projection )
        pszPrettyWkt = hSRS.ExportToPrettyWkt(False)
        return pszPrettyWkt
    except:
        return None

def get_raster_geotransform(raster_file):
    try:
        raster_geotransform = raster_file.GetGeoTransform()
        return raster_geotransform
    except:
        return None

def get_raster_origin(raster_geotransform):
    try:
        raster_origin = (raster_geotransform[0], raster_geotransform[3])
        return raster_origin
    except Exception:
        return None

def get_raster_pixle_size(raster_geotransform):
    try:
        raster_pixle_size = (raster_geotransform[1], raster_geotransform[5])
        return raster_pixle_size
    except:
        return None



def run_tif_info(file_path):
    layers = []
    raster_file = open_tif(file_path)     #To open raster file
    file_name = get_tif_name(raster_file)     #To print file name
    file_format = get_tif_format(raster_file)     #To print file format
    raster_number_of_band = get_raster_number_of_band(raster_file)
    raster_x_y_size = get_raster_x_y_size(raster_file)
    raster_projection = get_raster_projection(raster_file)
    raster_geotransform = get_raster_geotransform(raster_file)
    raster_origin = get_raster_origin(raster_geotransform)
    raster_pixle_size = get_raster_pixle_size(raster_geotransform)

    return {'file_name':file_name, 'file_format':file_format , 'num_band':str(raster_number_of_band),\
            'raster_x_y_size':raster_x_y_size, 'raster_projection':raster_projection,\
    'raster_geotransform':raster_geotransform, 'raster_origin':raster_origin,\
    'raster_pixle_size':raster_pixle_size}