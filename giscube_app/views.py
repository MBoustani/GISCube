import glob, os
from os.path import isfile
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from giscube.config import BASE_DIR, MEDIA_ROOT, MEDIA_URL
from giscube_app.models import Document
from giscube_app.forms import DocumentForm

from giscube_app.scripts.shp_name_info import run_shp_info
from giscube_app.scripts.tif_name_info import run_tif_info
from giscube_app.scripts.shp_to_kml import shp_to_kml
from giscube_app.scripts.gtif_to_kml import gtif_to_kml


def data_resource(request):
    ALL_FILES = os.listdir(MEDIA_ROOT + MEDIA_URL)
    UPLODED_FILES = [each for each in ALL_FILES if os.path.isfile(each)]
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            #get uploaded file name
            uploaded_file_name = newdoc.docfile.name
            file_extension = uploaded_file_name.split('.')[-1]
            if file_extension == "shp": #TODO: Use GDLA file format to recognize shapefiles, not with parsing
                file_name_without_ext = uploaded_file_name.replace('.{0}'.format(file_extension),'')
                shx_file = "{0}{1}{2}.shx".format(MEDIA_ROOT, MEDIA_URL, file_name_without_ext)
                dbf_file = "{0}{1}{2}.dbf".format(MEDIA_ROOT, MEDIA_URL, file_name_without_ext)
                if os.path.isfile(shx_file) == False:
                    print "shx does not exists"
                if os.path.isfile(dbf_file) == False:
                    print "dbf does not exists"
                newdoc.save()
            else:
                newdoc.save()

            return HttpResponseRedirect(reverse('giscube_app.views.data_resource'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render_to_response(
        'data_resource/index.html',
        {'documents': documents, 'form': form, 'UPLODED_FILES': UPLODED_FILES},
        context_instance=RequestContext(request)
    )


def data_information(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_file_name = [each for each in glob.glob("*.shp") ]
    shps_info = []    
    for name in shp_file_name:
        shps_info.append(run_shp_info(name))

    tif_file_name = [each for each in glob.glob("*.tif") ]
    tifs_info = []
    for name in tif_file_name:
        tifs_info.append(run_tif_info(name))

    context = {'shps_info': shps_info, 'tifs_info': tifs_info}
    
    return render(request, 'data_information/index.html', context)


def data_visualiser(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_kmls_names = []
    gtif_kmls_names = []
    shp_file_name = [each for each in glob.glob("*.shp") ] #TODO: Use GDLA file format to recognize shapefiles, not with parsing
    gtif_file_name = [each for each in glob.glob("*.tif") ] #TODO: Use GDLA file format to recognize geotif, not with parsing
    for name in shp_file_name:
        kml_file = shp_to_kml(name)
        shp_kmls_names.append(kml_file.split('.kml')[0])
    for name in gtif_file_name:
        kml_file = gtif_to_kml(name)
        gtif_kmls_names.append(kml_file.split('.kml')[0])
    context = {'shp_kmls_names':shp_kmls_names, 'gtif_kmls_names':gtif_kmls_names}
    return render(request, 'data_visualiser/index.html', context)


def tools(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_file_name = [each for each in glob.glob("*.shp") ]
    shps_info = []
    for name in shp_file_name:
        shps_info.append(run_shp_info(name))
    if shps_info:
        pass
    else:
        shps_info = ""
    context = {'shps_info': shps_info}

    return render(request, 'tools/index.html', context)
