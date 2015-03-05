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