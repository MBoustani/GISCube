from django import template

register = template.Library()

@register.filter(name='file_name')
def file_name(dict):
    return dict['file_name']

@register.filter(name='file_format')
def file_format(dict):
    return dict['file_format']

@register.filter(name='num_layer')
def num_layer(dict):
    return dict['num_layer']

@register.filter(name='layer_name')
def layer_name(dict):
    return dict['layer_name']

@register.filter(name='number_of_feature')
def number_of_feature(dict):
    return dict['number_of_feature']

@register.filter(name='layer_type')
def layer_type(dict):
    return dict['layer_type']

@register.filter(name='layer_spatial_reference')
def layer_spatial_reference(dict):
    return dict['layer_spatial_reference']

@register.filter(name='layer_extend')
def layer_extend(dict):
    return dict['layer_extend']