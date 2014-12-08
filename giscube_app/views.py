import glob, os
from os.path import isfile
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from giscube.config import MEDIA_ROOT, MEDIA_URL

from giscube_app.models import Document
from giscube_app.forms import DocumentForm

from giscube_app.scripts.open_file import open_shp_file, open_tif_file
from giscube_app.scripts.metadata import run_shp_info
from giscube_app.scripts.metadata import run_tif_info
from giscube_app.scripts.what_file import what_format
from giscube_app.scripts.conversion import get_geojson
from giscube_app.scripts.metadata import run_nc_info
from giscube_app.scripts.gtif_to_tile import create_gtif

#resource page
def data_resource(request):
    ALL_FILES = [each for each in os.listdir(MEDIA_ROOT+MEDIA_URL)]# if os.path.isfile(each)]
    UPLODED_FILES = []
    for each in ALL_FILES:
        print each
        print "----"
        file_format = what_format(MEDIA_ROOT+MEDIA_URL+each)
        print file_format
        print "____"
        if file_format == "ESRI Shapefile" and each.split(".")[-1]=="shp":
            UPLODED_FILES.append(each)
        elif file_format == "LIBKML" or file_format=="Kml Super Overlay":
            UPLODED_FILES.append(each)
        elif file_format == "GeoTIFF":
            UPLODED_FILES.append(each)
        elif file_format == "GeoJSON":
            UPLODED_FILES.append(each)
        elif file_format == "Network Common Data Format":
            UPLODED_FILES.append(each)
        elif each.split(".")[-1] == "txt" or each.split(".")[-1] == "csv":
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
        if open_tif_file(name): #netCDF file can be opened by GDAL
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
    ncs = []
    nc_variables = []
    geotifs = []
    shp_error = ""
    tif_error = ""
    nc_error = ""
    shp_file_name = [each for each in glob.glob("*.shp")] #TODO: Use GDLA file format to recognize shapefiles, not with parsing
    gtif_file_name = [each for each in glob.glob("*.tif")] #TODO: Use GDLA file format to recognize geotif, not with parsing
    nc_file_name = [each for each in glob.glob("*.nc")]
    json_file_name = [each for each in glob.glob("*.json")]
    for name in shp_file_name:
        if open_shp_file(name):
            json_name = get_geojson(name)
            shp_error = ""
        else:
            shp_error = "Cannot open shapfile."
            break
    for name in nc_file_name:
        if open_tif_file(name): #netCDF file can be opened by GDAL
            #json_name = get_geojson(name)
            nc_variables = sorted(run_nc_info(name)['all_variables'], key=str.lower)
            ncs.append(name)
            nc_error = ""
        else:
            nc_error = "Cannot open netCDF."
            break
    for name in gtif_file_name:
        if open_tif_file(name):
            geotif_folder = create_gtif(name)
            geotifs.append(geotif_folder)
            tif_error = ""
        else:
            tif_error = "Cannot open GeoTIFF."
            break
    #add all GeoJSON to jsons
    for json in json_file_name:
        jsons.append(json.split(".json")[0])

    context = {'jsons':jsons,'ncs':ncs, 'nc_variables':nc_variables, 'geotifs':geotifs, 'shp_error':shp_error, 'tif_error':tif_error, 'nc_error':nc_error}
    return render(request, 'data_visualiser/index.html', context)

#tools page
def tools(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_file_name = [each for each in glob.glob("*.shp") ]
    gtif_file_name = [each for each in glob.glob("*.tif")]
    nc_file_name = [each for each in glob.glob("*.nc")]
    shps_info = []
    tiffs_info = []
    netcdf_info = []
    ncs = []
    nc_variables = []
    for name in shp_file_name:
        if open_shp_file(name):
            shps_info.append(run_shp_info(name))
    for name in gtif_file_name:
        if open_tif_file(name):
            tiffs_info.append(run_tif_info(name))
    for name in nc_file_name:
        netcdf_info.append(run_nc_info(name))
    for name in nc_file_name:
        if open_tif_file(name): #netCDF file can be opened by GDAL
            nc_variables = sorted(run_nc_info(name)['all_variables'], key=str.lower)
            ncs.append(name)
            nc_error = ""
        else:
            nc_error = "Cannot open netCDF."
            break
    context = {'shps_info': shps_info, 'tiffs_info':tiffs_info, 'netcdf_info':netcdf_info, 'ncs':ncs, 'nc_variables':nc_variables,}

    return render(request, 'tools/index.html', context)
