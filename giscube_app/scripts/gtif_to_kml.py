import os

def gtif_to_kml(gtif_in):
    kml_out = gtif_in.replace('tif', 'kml')
    string = 'gdal_translate -of KMLSUPEROVERLAY -co "TILED=YES" {0} {1}'.format(gtif_in, kml_out)
    os.system(string)
    
    return kml_out