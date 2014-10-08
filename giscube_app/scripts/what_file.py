try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr

from gdalconst import GA_ReadOnly



def what_format(file_path):
    '''
    Open either raster or vector file and return format of it
    '''
    try:
        dataset = ogr.Open(file_path, not False )
        driver_name = dataset.GetDriver().GetName()
        return driver_name
    except:
        driver_name = "Format not found."

    try:
        dataset = gdal.Open(file_path, GA_ReadOnly)
        driver_name = dataset.GetDriver().LongName
        return driver_name
    except:
        driver_name = "Format not found."

    return driver_name