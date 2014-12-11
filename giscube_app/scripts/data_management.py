import os


def change_geotiff_resolution(selected_geotiff, geotiff_new_x_res, geotiff_new_y_res, geotiff_new_resolution_name):
    string = "gdalwarp -tr {0} {1} {2} {3}".format(geotiff_new_x_res, geotiff_new_y_res, selected_geotiff, geotiff_new_resolution_name)
    os.system(string)