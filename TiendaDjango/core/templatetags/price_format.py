from django import template

register = template.Library()

@register.filter
def miles(value):
    try:
        n = int(round(float(value)))
        return "{:,}".format(n).replace(",", ".")
    except (ValueError, TypeError):
        return value
