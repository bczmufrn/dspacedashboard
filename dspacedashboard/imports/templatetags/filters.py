import re

from django import template

register = template.Library()

@register.filter(name='format_output')
def format_output(value):
    value = value.strip()
    if value.startswith('Adding item from directory'):
        return f'<span class="font-weight-bold text-primary">\
            <i class="fas fa-arrow-right"></i> {value}</span>'

    elif value.startswith('Bitstream:'):
        return f'<b>{value}</b>'

    elif 'Owning  Collection:' in value:
        return f'<span class="text-success font-weight-bold">{value}</span>'
   
    elif 'Exception:' in value:
        result = re.match(r'(.*Exception:)(.*)', value)
        return f'<span class="text-danger text-bigger">\
            <i class="fas fa-exclamation-triangle"></i> \
            {result.groups()[0]}{result.groups()[1]}</span>' if result else value

    else:
        result = re.match(r'(Schema:.*Value:)(.*)', value)
        return f'<span class="font-weight-bold">{result.groups()[0]}</span>\
            {result.groups()[1]}' if result else value