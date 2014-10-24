from django import template

register = template.Library()

@register.filter(name='file_name')
def file_name(dict):
    return dict['file_name']

@register.filter(name='all_variables_info')
def all_variables_info(dict):
    return dict['all_variables_info']

@register.filter(name='var_name')
def var_name(dict):
    return dict.keys()[0]

@register.filter(name='attributes')
def attributes(dict):
    info = []
    for each in dict:
        for att in dict[each]:
            info.append('{0}: {1}'.format(att, dict[each][att]))
    return info