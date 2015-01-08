import os
from what_file import what_format
from shp_name_info import run_shp_info


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


def nc_to_gtif(latitudes, longitudes, values, geotiff_name):
    print "Creating GeoTIFF"
    file_format = "GTiff"
    driver = gdal.GetDriverByName(file_format)

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

    #print "Rotating GeoTIFF"
    #values = numpy.rot90(values, 1)

    print "Setting projection for GeoTIFF"

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    number_of_band = 1
    raster_type = gdal.GDT_Float32

    print "Creating raster dataset"

    raster_dataset = driver.Create(geotiff_name,
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


def nc_to_geojson(latitudes, longitudes, values, geotiff_name):
    print "Creating GeoJSON from netCDF"
    #multipoint = ogr.Geometry(ogr.wkbMultiPoint)
    print "multipoint geometry made"
    with open('{0}.json'.format(geotiff_name.split(".")[0]), 'w') as json:
        json.write('''{"type": "FeatureCollection","features": [''')
        string = ""
        for ilat, lat in enumerate(latitudes):
            for ilon, lon in enumerate(longitudes):
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(float(lon), float(lat))
                geojson_point = point.ExportToJson()
                #multipoint.AddGeometry(point)
                string += '{"type": "Feature","geometry":'
                string += geojson_point
                string += ',"properties": {"prop0": "'
                string += "{0}".format(values[ilat][ilon])
                string += '"}},'
        string = string[:-1] + ']}'
        json.write(string)
    json.close()
    print "netCDF to GeoJSON, Done"


def convert_vector_to_geojson(GeoJSON_file_name, vector_path):
    #string = "ogr2ogr -f GeoJSON -t_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs'\
    #        -lco \"WRITE_BBOX=YES\" {0} {1} ".format(GeoJSON_file_name, vector_path)
    string = "ogr2ogr -f GeoJSON -t_srs EPSG:4326 -lco \"WRITE_BBOX=YES\" {0} {1} ".format(GeoJSON_file_name, vector_path)
    os.system(string)

    return GeoJSON_file_name


def get_geojson(vector_path):
    vector_format = what_format(vector_path)
    if vector_format == "ESRI Shapefile":
        vector_name = run_shp_info(vector_path)['layer_name']
    GeoJSON_file_name = vector_name + "_wgs84.json"
    if not os.path.isfile(GeoJSON_file_name):
        convert_vector_to_geojson(GeoJSON_file_name, vector_path)
        return GeoJSON_file_name


def shp_to_kml(shp_path, kml_name):
    try:
        shp_datasource = ogr.Open(shp_path)
    except:
        raise "Shapefile cannot be opened"
        sys.exit()

    driver = ogr.GetDriverByName('KML')
    layer_name = 'kml_layer'
    kml_datasource = driver.CreateDataSource(kml_name)
    
    layer = shp_datasource.GetLayerByIndex(0)
    srs = layer.GetSpatialRef()
    geom_type = layer.GetGeomType()
    kml_layer = kml_datasource.CreateLayer(layer_name, srs, geom_type)

    layer_number = shp_datasource.GetLayerCount()
    for each in range(layer_number):
        layer = shp_datasource.GetLayerByIndex(each)
        features_number = layer.GetFeatureCount()
        for i in range(features_number):
            shp_feature = layer.GetFeature(i)
            feature_geometry = shp_feature.GetGeometryRef()
            kml_feature = ogr.Feature(kml_layer.GetLayerDefn())
            kml_feature.SetGeometry(feature_geometry)
            kml_layer.CreateFeature(kml_feature)


def convert_geotiff_to_kml(selected_geotiff, geotiff_to_kml_name):
    string = "gdal_translate -of KMLSUPEROVERLAY {0} {1}".format(selected_geotiff, geotiff_to_kml_name)
    os.system(string)