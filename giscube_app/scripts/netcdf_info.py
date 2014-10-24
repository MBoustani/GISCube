#!/usr/bin/env python

#Project:       Geothon (https://github.com/MBoustani/Geothon)
#File:          raster_info.py
#Description:   This code prints general informations for a given raster data.
#Date:          10/06/2013
#Author:        Maziyar Boustani (github.com/MBoustani)

from netCDF4 import Dataset
import numpy as np

def get_nc_data(nc_file, latitude_var, longitude_var, time_var, value_var, selected_time_index):
    print nc_file
    nc_dataset = open_file(nc_file)
    if nc_dataset:
        lat = nc_dataset.variables[latitude_var]
        lon = nc_dataset.variables[longitude_var]
        time = nc_dataset.variables[time_var]
        value = nc_dataset.variables[value_var]
        
        lat_dim = lat.dimensions
        lon_dim = lon.dimensions
        time_dim = time.dimensions
        value_dim = value.dimensions

        lat_shape = lat.shape
        lon_shape = lon.shape
        time_shape = time.shape
        value_shape = value.shape

        print 'Latitude shape: {0}'.format(lat_shape)
        print 'Longitude shape: {0}'.format(lon_shape)
        print 'Time shape: {0}'.format(time_shape)
        print 'Value shape: {0}'.format(value_shape)

        print "Getting dimensions info"
        dims_info = {}
        for i, each in enumerate(lat_dim):
            dims_info[each] = lat_shape[i]

        for i, each in enumerate(lon_dim):
            dims_info[each] = lon_shape[i]

        for i, each in enumerate(time_dim):
            dims_info[each] = time_shape[i]

        print "Slicing vlaues"
        slices = ()
        for dim in value_dim:
            if dim in dims_info:
                if dim in time_dim:
                    slices += (slice(selected_time_index,selected_time_index+1),)
                else:
                    slices += (slice(0,dims_info[dim]+1),)
            else:
                slices += (slice(0,1),)
        print "Values sliced"
        print np.squeeze(value[slices]).shape
        return np.squeeze(value[slices])

def open_file(file_path):
    try:
        nc_file = Dataset(file_path, mode='r')
        if not nc_file:
            raise "File cannot be opened"
        return nc_file
    except:
        raise "File cannot be opened"
        sys.exit()

def get_variables(nc_file):
    if nc_file:
        return [variable.encode() for variable in nc_file.variables.keys()]


def get_file_name(file_path):
    if file_path:
        return file_path


def variables_info(nc_file, all_variables):
    variables_info = []
    for value in all_variables:
        variable = nc_file.variables[value]
        each_variable = {}
        each_variable[value] = {}
        each_variable[value]['dimensions'] = variable.dimensions
        for att in variable.ncattrs():
            each_variable[value][att] = variable.getncattr(att)
        variables_info.append(each_variable)

    return variables_info


def run_nc_info(file_path):
    nc_file = open_file(file_path)
    file_name = get_file_name(file_path)
    all_variables = get_variables(nc_file)
    all_variables_info  = variables_info(nc_file, all_variables)

    return {'file_name':file_name, 'all_variables':all_variables, 'all_variables_info':all_variables_info}