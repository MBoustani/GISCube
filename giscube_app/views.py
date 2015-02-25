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
from giscube_app.scripts.metadata import get_nc_metadata, get_hdf_metadata
from giscube_app.scripts.gtif_to_tile import create_gtif

#resource page
def data_resource(request, uploaded=''):
    notification = ""
    ALL_FILES = [each for each in os.listdir(MEDIA_ROOT+MEDIA_URL)]
    UPLODED_FILES = []
    for each in ALL_FILES:
        file_format = what_format(MEDIA_ROOT+MEDIA_URL+each)
        print file_format
        if each.split(".")[-1]=="shp":
            UPLODED_FILES.append(each)
        if each.split(".")[-1]=="shx":
            UPLODED_FILES.append(each)
        if each.split(".")[-1]=="dbf":
            UPLODED_FILES.append(each)
        if each.split(".")[-1]=="prj":
            UPLODED_FILES.append(each)
        elif file_format == "LIBKML" or file_format=="Kml Super Overlay":
            UPLODED_FILES.append(each)
        elif file_format == "GeoTIFF":
            UPLODED_FILES.append(each)
        elif file_format == "GeoJSON":
            UPLODED_FILES.append(each)
        elif file_format == "Network Common Data Format":
            UPLODED_FILES.append(each)
        elif file_format == "NetCDF":
            UPLODED_FILES.append(each)
        elif file_format == "Hierarchical Data Format Release 4":
            UPLODED_FILES.append(each)
        elif file_format == "Hierarchical Data Format Release 5":
            UPLODED_FILES.append(each)
        elif each.split(".")[-1] == "txt" or each.split(".")[-1] == "text" or each.split(".")[-1] == "csv" or each.split(".")[-1] == "ascii":
            UPLODED_FILES.append(each)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            uploaded_file_name = newdoc.docfile.name
            newdoc.save()

            return HttpResponseRedirect('/resource/{0}'.format(uploaded_file_name))
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    if uploaded.split('.')[-1] == 'shp':
        file_name_without_ext = uploaded.replace('.{0}'.format(uploaded.split('.')[-1]),'')
        shx_file = "{0}{1}{2}.shx".format(MEDIA_ROOT, MEDIA_URL, file_name_without_ext)
        if os.path.isfile(shx_file) == False:
            notification = 'Please upload files below to complete Shapefile:\n{0}.shx{0}.dbf{0}.prj'.format(file_name_without_ext)
    return render_to_response(
        'data_resource/index.html',
        {'documents': documents, 'form': form, 'UPLODED_FILES': UPLODED_FILES, 'notification':notification},
        context_instance=RequestContext(request)
    )

#information page
def data_information(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_file_name = [each for each in glob.glob("*.shp") ]
    shps_info = []
    shp_error = "No Shapefile"
    tif_error = "No GeoTIFF"
    nc_error = "No netCDF"
    hdf_error = "No HDF"
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
    ncs_metadata = []
    for name in nc_file_name:
        if get_nc_metadata(name):
            ncs_metadata.append(get_nc_metadata(name))
            nc_error = ""
        else:
            nc_error = "Cannot open netCDF file."
            break

    hdf_file_name = [each for each in glob.glob("*.he5") ]
    hdfs_metadata = []
    for name in hdf_file_name:
        if get_hdf_metadata(name):
            hdfs_metadata.append(get_hdf_metadata(name))
            hdf_error = ""
        else:
            hdf_error = "Cannot open HDF file."
            break

    context = {'shps_info': shps_info,
               'tifs_info': tifs_info,
               'ncs_metadata':ncs_metadata,
               'hdfs_metadata':hdfs_metadata,
               'shp_error':shp_error,
               'tif_error':tif_error,
               'nc_error':nc_error,
               'hdf_error':hdf_error
               }
    
    return render(request, 'data_information/index.html', context)

#visualiser page
def data_visualiser(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    jsons = []
    geotifs = []
    shp_error = ""
    tif_error = ""
    shp_file_name = [each for each in glob.glob("*.shp")] #TODO: Use GDLA file format to recognize shapefiles, not with parsing
    gtif_file_name = [each for each in glob.glob("*.tif")] #TODO: Use GDLA file format to recognize geotif, not with parsing
    json_file_name = [each for each in glob.glob("*.json")]

    #add all GeoJSON to jsons
    for json in json_file_name:
        jsons.append(json.split(".json")[0])

    for name in shp_file_name:
        if open_shp_file(name):
            json_name = get_geojson(name)
            if json_name:
                jsons.append(json_name.split(".json")[0])
            shp_error = ""
        else:
            shp_error = "Cannot open shapfile."
            break

    for name in gtif_file_name:
        if open_tif_file(name):
            if os.path.exists('{0}{1}'.format(MEDIA_ROOT, MEDIA_URL) + name.split(".tif")[0]):
                geotifs.append(name.split(".tif")[0])
                tif_error = ""
            else:
                geotif_folder = create_gtif(name)
                geotifs.append(geotif_folder)
                tif_error = ""
        else:
            tif_error = "Cannot open GeoTIFF."
            break

    context = {'jsons':jsons, 'geotifs':geotifs, 'shp_error':shp_error, 'tif_error':tif_error}
    return render(request, 'data_visualiser/index.html', context)

#tools page
def tools(request):
    os.chdir(MEDIA_ROOT + MEDIA_URL)
    shp_file_name = [each for each in glob.glob("*.shp") ]
    gtif_file_name = [each for each in glob.glob("*.tif")]
    nc_file_name = [each for each in glob.glob("*.nc")]
    text_file_name = [each for each in glob.glob("*.txt") ] + [each for each in glob.glob("*.text") ]
    shps_info = []
    tiffs_info = []
    ncs_metadata = []
    text_info = []
    for name in shp_file_name:
        if open_shp_file(name):
            shps_info.append(run_shp_info(name))
    for name in gtif_file_name:
        if open_tif_file(name):
            tiffs_info.append(run_tif_info(name))
    for name in nc_file_name:
        if open_tif_file(name):
            nc_metadata = get_nc_metadata(name)
            ncs_metadata.append(nc_metadata)
            nc_error = ""
        else:
            nc_error = "Cannot open netCDF."
            break
    for name in text_file_name:
        text_info.append(name)
    context = {'shps_info': shps_info, 'tiffs_info':tiffs_info, 'ncs_metadata':ncs_metadata, 'text_file_name':text_file_name}

    return render(request, 'tools/index.html', context)
