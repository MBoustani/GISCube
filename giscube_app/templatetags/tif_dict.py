from django import template

register = template.Library()

@register.filter(name='file_name')
def file_name(dict):
    return dict['file_name']

@register.filter(name='file_format')
def file_format(dict):
    return dict['file_format']

@register.filter(name='layer_name')
def layer_name(dict):
    return dict['layer_name']

@register.filter(name='num_band')
def num_layer(dict):
    return dict['num_band']

@register.filter(name='raster_x_y_size')
def raster_x_y_size(dict):
    return dict['raster_x_y_size']

@register.filter(name='raster_projection')
def number_of_feature(dict):
    return dict['raster_projection']

@register.filter(name='raster_geotransform')
def layer_type(dict):
    return dict['raster_geotransform']

@register.filter(name='raster_origin')
def layer_spatial_reference(dict):
    return dict['raster_origin']

@register.filter(name='raster_pixle_size')
def layer_extend(dict):
    return dict['raster_pixle_size']