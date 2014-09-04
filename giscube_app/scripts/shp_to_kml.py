import os

def shp_to_kml(shp_in):
    kml_out = shp_in.replace('shp', 'kml')
    string = 'ogr2ogr -f KML {0} {1}'.format(kml_out, shp_in)
    os.system(string)
    
    return kml_out