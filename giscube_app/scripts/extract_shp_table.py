#!/usr/bin/env python

'''
Project:       Geothon (https://github.com/MBoustani/Geothon)
File:          Vector/export_shp_att_csv.py
Description:   This code exports Shapefile attribute table to csv file
Author:        Maziyar Boustani (github.com/MBoustani)
'''
import csv
import argparse

try:
    import ogr
except ImportError:
    from osgeo import ogr

def extract_shp_table(shp_file_name, csv_file_name):
    #set the driver to ESRI Shapefiel
    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    #open shapefile
    shp_datasource = driver.Open(shp_file_name)
    
    #get shapefile layer
    layer = shp_datasource.GetLayerByIndex(0)
    
    #get shapefile layer definition
    layer_defn = layer.GetLayerDefn()
    
    #get number of fields(columns) from shapefile attribute table
    num_field_col = layer_defn.GetFieldCount()
    
    #create csv file to store shapefile attribute table
    with open(csv_file_name, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        #store field header
        field_name = []
        for field in range(num_field_col):
            field_name.append(layer_defn.GetFieldDefn(field).GetName())
        writer.writerow(field_name)
    
        #store attribute from each feature
        num_feature = layer.GetFeatureCount()
        for each in range(num_feature):
            feautre = layer.GetFeature(each)
            feautre_name = []
            for i in range(num_field_col):
                feautre_name.append(feautre.GetFieldAsString(i))
            writer.writerow(feautre_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-shp','--shp', help='Description for foo argument', required=True)
    parser.add_argument('-text_name','--text_name', help='Description for bar argument', required=True)
    args = vars(parser.parse_args())
    shp_file_name = args['shp']
    csv_file_name = args['text_name']
    extract_shp_table(shp_file_name, csv_file_name)