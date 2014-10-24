try:
    import gdal
except ImportError:
    from osgeo import gdal

try:
    import ogr
except ImportError:
    from osgeo import ogr

from osgeo import osr


import numpy
from numpy import ma


def nc_to_gtif(latitudes, longitudes, values):
    print "Creating GeoTIFF"
    file_format = "GTiff"
    driver = gdal.GetDriverByName(file_format)
    
    GEOTIFF_OUTPUT = "netCDF_in_geotiff.tif"

    print "Getting values for making GeoTIFF"

    try:
        values = ma.array(values).data
    except:
        pass

    print "Converting longitudes"
    
    for i in range(len(longitudes)):
        if longitudes[i] > 180:
            longitudes[i] = longitudes[i] - 360

    print "Calculating pixel size"

    raster_x_size = longitudes.shape[0]
    raster_y_size = latitudes.shape[0]

    print "Rotating GeoTIFF"

    values = numpy.rot90(values, 1)

    print "Setting projection for GeoTIFF"

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    number_of_band = 1
    raster_type = gdal.GDT_Float32

    print "Creating raster dataset"

    raster_dataset = driver.Create(GEOTIFF_OUTPUT,
                                   raster_x_size,
                                   raster_y_size,
                                   number_of_band,
                                   raster_type)

    raster_dataset.GetRasterBand(1).WriteArray(values)

    latitude_pixel_size = (abs(min(latitudes)) + abs(max(latitudes))) / len(latitudes)
    longitude_pixel_size = (abs(min(longitudes)) + abs(max(longitudes))) / len(longitudes) 
    
    raster_dataset.SetGeoTransform((min(longitudes), latitude_pixel_size, 0, min(latitudes), 0, longitude_pixel_size))
    raster_dataset.SetProjection(srs.ExportToWkt())

    print "GeoTIFF Created"

def nc_to_geojson(latitudes, longitudes, values):
    print "Creating GeoJSON from netCDF"
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)
    print "multipoint geometry made"
    for lat in latitudes:
        for lon in longitudes:
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(lon, lat)
            multipoint.AddGeometry(point)
    print "point data read sucessfully"

    geojson_multipoint = multipoint.ExportToJson()
    with open('out.json', 'w') as json:
        json.write(geojson_multipoint)
    json.close()
    print "netCDF to GeoJSON, Done"
    