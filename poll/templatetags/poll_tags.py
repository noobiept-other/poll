from django import template

register = template.Library()

@register.filter
def percentage( votes, total_votes ):

    if total_votes == 0:
        value = 0

    else:
        value = float( votes ) / float( total_votes ) * 100.0

    return '{:.2f} %'.format( value )
