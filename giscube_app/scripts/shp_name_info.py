#!/usr/bin/env python

#Project:       Geothon (https://github.com/MBoustani/Geothon)
#File:          vector_info.py
#Description:   This code prints general informations for a given vector data.
#Date:          10/03/2013
#Author:        Maziyar Boustani (github.com/MBoustani)


import sys
import argparse
try:
    from osgeo import ogr
except ImportError:
    import ogr


def open_file(file_path):
    try:
        vector_file = ogr.Open(file_path)
        if not vector_file:
            raise "File cannot be opened"
        return vector_file
    except:
        raise "File cannot be opened"
        sys.exit()

def get_file_name(vector_file):
    try:
        file_name = vector_file.GetName()
        return file_name
    except:
        return None

def get_file_format(vector_file):
    try:
        file_format = vector_file.GetDriver().GetName()
        return file_format
    except:
        return None

def get_file_number_of_layers(vector_file):
    try:
        number_of_layers = vector_file.GetLayerCount()
        return number_of_layers
    except:
        return None

def get_layer(vector_file, layer_index):
    try:
        layer = vector_file.GetLayerByIndex(layer_index)
        return layer
    except:
        return None

def get_layer_name(layer_file):
    try:
        layer_name = layer_file.GetName()
        return layer_name
    except:
        return None

def get_number_of_feature(layer_file):
    try:
        number_of_feature = layer_file.GetFeatureCount()
        return number_of_feature 
    except:
        return None

def get_layer_type(layer_file):
    try:
        geom_type_index = layer_file.GetLayerDefn().GetGeomType()
        layer_type = ogr.GeometryTypeToName(geom_type_index)
        return layer_type
    except:
        return None

def get_layer_spatial_reference(layer_file):
    try:
        layer_spatial_reference = layer_file.GetSpatialRef().ExportToPrettyWkt()
        return layer_spatial_reference
    except:
        return None

def get_layer_extend(layer_file):
    try:
        layer_extend = layer_file.GetExtent()
        return layer_extend
    except:
        return None


def run_shp_info(file_path):
    layers = []
    vector_file = open_file(file_path)     #To open vector file
    file_name = get_file_name(vector_file)     #To print file name
    file_format = get_file_format(vector_file)     #To print file format
    file_number_of_layers = get_file_number_of_layers(vector_file)     #To print number of layer/s
    for layer_index in range(file_number_of_layers):
        layer = {}
        layer_file = get_layer(vector_file, layer_index)
        layer['layer file'] = layer_file
        layer_name = get_layer_name(layer_file)
        layer['layer name'] = layer_name
        number_of_feature = get_number_of_feature(layer_file)
        layer['number of feature'] = number_of_feature
        layer_type = get_layer_type(layer_file)
        layer['layer type'] = layer_type
        layer_spatial_reference = get_layer_spatial_reference(layer_file)
        layer['layer spatial reference'] = layer_spatial_reference
        layer_extend = get_layer_extend(layer_file)
        layer['layer extend'] = layer_extend
        layers.append(layer)
    
    return {'file_name':file_name, 'file_format':file_format , 'num_layer':str(file_number_of_layers),\
            'layer_name':layer['layer name'], 'number_of_feature':layer['number of feature'],\
    'layer_type':layer['layer type'], 'layer_spatial_reference':layer['layer spatial reference'],\
    'layer_extend':layer['layer extend']}
