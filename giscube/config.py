import os

#get the current directory
Current_path = os.getcwd()

STATIC_ROOT = ''
STATIC_URL = '/static/'
BASE_DIR = '{0}/giscube_app/static/'.format(Current_path)
MEDIA_ROOT = '{0}/giscube_app/static/'.format(Current_path)
MEDIA_URL = 'uploaded_files/'