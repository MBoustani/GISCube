#!/usr/bin/env python

try:
    from osgeo import ogr
except ImportError:
    import ogr

try:
    from osgeo import gdal
    from osgeo import osr
except ImportError:
    import gdal
    import osr


def open_shp_file(file_path):
    try:
        vector_file = ogr.Open(file_path)
        return vector_file
    except:
        return False


def open_tif_file(file_path):
    try:
        raster_file = gdal.Open(file_path)
        return raster_file
    except:
        return False