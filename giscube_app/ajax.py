import os, shutil
from dajaxice.decorators import dajaxice_register
from giscube.config import BASE_DIR, MEDIA_ROOT, MEDIA_URL

@dajaxice_register(method='GET')
def remove_loaded_file(request, param):
    Uploaded_file = MEDIA_ROOT + MEDIA_URL + param
    os.remove(Uploaded_file)
    #and remove the associated folder for a file is exists
    try:
        shutil.rmtree('{0}'.format(Uploaded_file[:-4]))
    except:
        pass
    
    
@dajaxice_register(method='GET')
def reproject_vector(request, selected_vector, selected_proj, vector_name):

    s = 'ogr2ogr -f "ESRI Shapefile" -s_srs EPSG:27700 -t_srs EPSG:4326 {0} {1}'.format(MEDIA_ROOT+MEDIA_URL+vector_name, MEDIA_ROOT+MEDIA_URL+selected_vector+'.shp')
    os.system(s)