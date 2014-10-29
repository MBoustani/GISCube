from django import template

register = template.Library()

@register.filter(name='file_name')
def file_name(dict):
    return dict['file_name']