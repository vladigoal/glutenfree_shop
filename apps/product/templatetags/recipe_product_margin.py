from django import template
register = template.Library()

@register.filter(name='recipe_product_margin')
def recipe_product_margin(d, index):
    if index % 4 == 1:
        return 'nomargin'
    else:
        return ''