# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter(needs_autoescape=True)
def currency(dollars, autoescape=None):
    dollars = round(float(dollars), 2)
    return mark_safe(u"%s%s <span>грн.</span>" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:]))


@register.filter()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price