import os


def convert_shp_to_geojson(GeoJSON_file_name, shapefile_path):
        string = "ogr2ogr -f GeoJSON -t_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs'\
                -lco \"WRITE_BBOX=YES\" {0} {1} ".format(GeoJSON_file_name, shapefile_path)
        os.system(string)

        return GeoJSON_file_name


def make_geojson_variable(GeoJSON_file_path, GeoJSON_layer_name):
        GeoJSON_file = open(GeoJSON_file_path, 'r')
        GeoJSON_file_text = GeoJSON_file.read()
        GeoJSON_file.close()
        GeoJSON_file = open(GeoJSON_file_path, 'w')
        GeoJSON_file.write("var {0} = ".format(GeoJSON_layer_name))
        GeoJSON_file.write(GeoJSON_file_text)
        GeoJSON_file.close()


def get_geojson(shp_path):
        GeoJSON_layer_name = shp_path.split(".shp")[0] 
        GeoJSON_file_name = GeoJSON_layer_name + ".json"
        if os.path.isfile(GeoJSON_file_name):
                pass
        else:
                GeoJSON = convert_shp_to_geojson(GeoJSON_file_name, shp_path)
                make_geojson_variable(GeoJSON, GeoJSON_layer_name)

        return GeoJSON_layer_name