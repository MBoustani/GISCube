#!/usr/bin/env python

#Project:       Geothon (https://github.com/MBoustani/Geothon)
#File:          raster_info.py
#Description:   This code prints general informations for a given raster data.
#Date:          10/06/2013
#Author:        Maziyar Boustani (github.com/MBoustani)


import sys
import argparse
try:
    from osgeo import gdal
    from osgeo import osr
except ImportError:
    import gdal
    import osr


def open_file(file_path):
    try:
        raster_file = gdal.Open(file_path)
        if not raster_file:
            raise "File cannot be opened"
        return raster_file
    except:
        raise "File cannot be opened"
        sys.exit()

def get_file_name(raster_file):
    try:
        file_name = raster_file.GetDescription()
        return file_name
    except:
        return None

def get_file_format(raster_file):
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

def get_layer_extend(layer_file):
    try:
        layer_extend = layer_file.GetExtent()
        return layer_extend
    except:
        return None



def run_tif_info(file_path):
    layers = []
    raster_file = open_file(file_path)     #To open raster file
    file_name = get_file_name(raster_file)     #To print file name
    file_format = get_file_format(raster_file)     #To print file format
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