import os
import shutil
from giscube.config import MEDIA_ROOT, MEDIA_URL
import subprocess

def create_gtif(gtif):
    UPLOADED_FILE_DIR = '{0}{1}'.format(MEDIA_ROOT, MEDIA_URL)
    gtif_path = UPLOADED_FILE_DIR + gtif
    gtif_folder = gtif.split(".tif")[0]
    string = "gdal2tiles.py {0} {1}".format(gtif_path, gtif_folder)
    subprocess.Popen(["gdal2tiles.py","{0}".format(gtif_path),"{0}".format(gtif_folder)])
    
    return gtif_folder