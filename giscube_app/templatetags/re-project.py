from django import template

register = template.Library()

@register.filter(name='re_poject_vector')
def re_poject_vector(lists):
    print lists
    #return dict['file_name']

@register.filter(name='file_format')
def re_rpoject_raster(dict):
    return dict['file_format']
