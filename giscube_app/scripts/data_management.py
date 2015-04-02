import os


def change_geotiff_resolution(selected_geotiff, geotiff_new_x_res, geotiff_new_y_res, geotiff_new_resolution_name):
    string = "gdalwarp -tr {0} {1} {2} {3}".format(geotiff_new_x_res, geotiff_new_y_res, selected_geotiff, geotiff_new_resolution_name)
    os.system(string)

def color_table_on_geotiff(selected_geotiff, selected_color_table, colored_geotiff_name):
    string = 'gdaldem color-relief {0} {1} {2} -alpha -of GTiff'.format(selected_geotiff, selected_color_table, colored_geotiff_name)
    os.system(string)