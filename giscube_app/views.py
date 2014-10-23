import glob, os
from os.path import isfile
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

#import variables
from giscube.config import MEDIA_ROOT, MEDIA_URL

#import form and model to be able to upload files
from giscube_app.models import Document
from giscube_app.forms import DocumentForm

#import GIS scripts
from giscube_app.scripts.open_file import open_shp_file, open_tif_file
from giscube_app.scripts.shp_name_info import run_shp_info
from giscube_app.scripts.tif_name_info import run_tif_info
from giscube_app.scripts.shp_to_kml import shp_to_kml
from giscube_app.scripts.gtif_to_kml import gtif_to_kml
from giscube_app.scripts.what_file import what_format
from giscube_app.scripts.vector_to_geojson import get_geojson
from giscube_app.scripts.netcdf_info import run_nc_info

#resource page
def data_resource(request):
    ALL_FILES = [each for each in os.listdir(MEDIA_ROOT+MEDIA_URL)]# if os.path.isfile(each)]
    UPLODED_FILES = []
    for each in ALL_FILES:
        file_format = what_format(MEDIA_ROOT+MEDIA_URL+each)
        if file_format == "ESRI Shapefile" and each.split(".")[-1]=="shp":
            UPLODED_FILES.append(each)
        elif file_format == "LIBKML":
            UPLODED_FILES.append(each)
        elif file_format == "GeoTIFF":
            UPLODED_FILES.append(each)
        elif file_format == "Network Common Data Format":
            UPLODED_FILES.append(each)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            #get uploaded file name
            uploaded_file_name = newdoc.docfile.name
            print uploaded_file_name
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

#information page
def data_information(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_file_name = [each for each in glob.glob("*.shp") ]
    shps_info = []
    shp_error = ""
    tif_error = ""
    nc_error = ""
    for name in shp_file_name:
        if open_shp_file(name):
            shps_info.append(run_shp_info(name))
            shp_error = ""
        else:
            shp_error = "Cannot open shapfile."
            break

    tif_file_name = [each for each in glob.glob("*.tif") ]
    tifs_info = []
    for name in tif_file_name:
        if open_tif_file(name):
            tifs_info.append(run_tif_info(name))
            tif_error = ""
        else:
            tif_error = "Cannot open tif file."
            break

    nc_file_name = [each for each in glob.glob("*.nc") ]
    nc_info = []
    for name in nc_file_name:
        if open_tif_file(name):
            nc_info.append(run_nc_info(name))
            nc_error = ""
        else:
            nc_error = "Cannot open netCDF file."
            break

    context = {'shps_info': shps_info, 'tifs_info': tifs_info, 'nc_info':nc_info, 'shp_error':shp_error, 'tif_error':tif_error, 'nc_error':nc_error}
    
    return render(request, 'data_information/index.html', context)

#visualiser page
def data_visualiser(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    jsons = []
    shp_error = ""
    tif_error = ""
    shp_file_name = [each for each in glob.glob("*.shp") ] #TODO: Use GDLA file format to recognize shapefiles, not with parsing
    gtif_file_name = [each for each in glob.glob("*.tif") ] #TODO: Use GDLA file format to recognize geotif, not with parsing
    #for name in shp_file_name:
    #    if open_shp_file(name):
    #        kml_file = shp_to_kml(name)
    #        shp_kmls_names.append(kml_file.split('.kml')[0])
    #        shp_error = ""
    #    else:
    #        shp_error = "Cannot open shapfile."
    #        break
    #for name in gtif_file_name:
    #    if open_tif_file(name):
    #        kml_file = gtif_to_kml(name)
    #        gtif_kmls_names.append(kml_file.split('.kml')[0])
    #        tif_error = ""
    #    else:
    #        tif_error = "Cannot open tif file."
    #        break
    for name in shp_file_name:
        if open_shp_file(name):
            json_name = get_geojson(name)
            jsons.append(json_name)
            shp_error = ""
        else:
            shp_error = "Cannot open shapfile."
            break
    context = {'jsons':jsons, 'shp_error':shp_error, 'tif_error':tif_error}
    return render(request, 'data_visualiser/index.html', context)

#tools page
def tools(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_file_name = [each for each in glob.glob("*.shp") ]
    shps_info = []
    for name in shp_file_name:
        if open_shp_file(name):
            shps_info.append(run_shp_info(name))   
    context = {'shps_info': shps_info}

    return render(request, 'tools/index.html', context)
