'''
custom template tag for the courses application.
determine which type of object each item is and
possibility to display each item in the template
differently.
'''

from django import template


register = template.Library()


@register.filter
def model_name(obj):
    try:
        # get the model of obj from the _meta attribute of the Meta class.
        return obj._meta.model_name
    except AttributeError:
        return None
