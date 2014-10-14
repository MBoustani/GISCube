import os
from what_file import what_format
from shp_name_info import run_shp_info

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
        GeoJSON_file_name = vector_name + ".json"
        if not os.path.isfile(GeoJSON_file_name):
                convert_vector_to_geojson(GeoJSON_file_name, vector_path)
        return vector_name
