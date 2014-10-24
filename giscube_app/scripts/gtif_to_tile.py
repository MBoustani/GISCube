import os
import shutil
from giscube.config import MEDIA_ROOT, MEDIA_URL

def create_gtif(gtif):
    UPLOADED_FILE_DIR = '{0}{1}'.format(MEDIA_ROOT, MEDIA_URL)
    gtif_path = UPLOADED_FILE_DIR + gtif
    gtif_folder = gtif.split(".tif")[0]
    if os.path.exists(UPLOADED_FILE_DIR + gtif_folder):
        pass
    else:
        #string = "gdal2tiles.py -s '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs' -n -z 2-6 {0} {1}".format(gtif_path, gtif_name)
        string = "gdal2tiles.py {0} {1}".format(gtif_path, gtif_folder)
        os.system(string)
    
    return gtif_folder