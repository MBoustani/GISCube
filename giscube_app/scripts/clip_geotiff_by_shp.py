import os

def clip_geotiff_by_shp(selected_geotiff, selected_shapefile, clipped_geotiff_name):
    string = "gdalwarp -cutline {0} -crop_to_cutline {1} {2}".format(selected_shapefile, selected_geotiff, clipped_geotiff_name)
    os.system(string)