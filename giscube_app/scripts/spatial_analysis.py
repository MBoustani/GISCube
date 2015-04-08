import os

try:
    import ogr
except ImportError:
    from osgeo import ogr

try:
    import osr
except ImportError:
    from osgeo import osr


def buffer_shapefile(selected_shp, buffer_shp_buffer_range, buffer_shp_out_name, buffer_shp_out_layername):
    if selected_shp.split(".")[-1] != "shp":
        selected_shp = selected_shp + ".shp"
    try:
        buffer_shp_buffer_range = float(buffer_shp_buffer_range)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        in_shp_datasource = driver.Open(selected_shp)
        in_layer = in_shp_datasource.GetLayer()
        in_srs = in_layer.GetSpatialRef()
        num_feature = in_layer.GetFeatureCount()
        out_shp_datasource = driver.CreateDataSource(buffer_shp_out_name)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        print in_srs
        print srs
        out_layer = out_shp_datasource.CreateLayer(buffer_shp_out_layername, in_srs, ogr.wkbMultiPolygon)
        for each in range(num_feature):
            in_feature = in_layer.GetFeature(each)
            in_geom = in_feature.GetGeometryRef()
            bufer_geom = in_geom.Buffer(buffer_shp_buffer_range)
            out_feature = ogr.Feature(out_layer.GetLayerDefn())
            out_feature.SetGeometry(bufer_geom)
            out_layer.CreateFeature(out_feature)
        return "Done."
    except:
        return "Someting went wrong"


def find_point_inside_feature(selected_vector, point_inside_shapefile_lat, point_inside_shapefile_lon):
    
    in_shp_datasource = ogr.Open("{0}.shp".format(selected_vector))
    in_layer = in_shp_datasource.GetLayerByIndex(0)
    in_layer_defn = in_layer.GetLayerDefn()
    num_field_col = in_layer_defn.GetFieldCount()

    try:
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(point_inside_shapefile_lon), float(point_inside_shapefile_lat))
    except:
        print "cannot create point geometry"

    try:
        field_name = []
        for field in range(num_field_col):
            field_name.append(in_layer_defn.GetFieldDefn(field).GetName())
    except:
        print "Cannot read feature attribute information"

    feature_info = "Point is not in any feature."
    features_number = in_layer.GetFeatureCount()
    for i in range(features_number):
        in_shp_feature = in_layer.GetFeature(i)
        in_feature_geometry = in_shp_feature.GetGeometryRef()
        if point.Within(in_feature_geometry):
            field_count = in_shp_feature.GetFieldCount()
            feature_info = ""
            for field in range(field_count):
                feature_info += "<h3>{0}: </h3> <p>{1}</p>".format(field_name[field], in_shp_feature.GetFieldAsString(field))
            break

    return feature_info
