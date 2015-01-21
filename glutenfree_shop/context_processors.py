# -*- coding: utf-8 -*-
import urllib
from django.utils import simplejson as json
from apps.product.models import Product, Category, Recipe

def cart(request):
    session = request.session
    ret = []
        
    if session.get("cart") == None:
        session['cart'] = ""
    
    if session['cart']:   
        cart = json.loads(urllib.unquote(session['cart']).decode('utf-8'))
        ids = []
        for prod in cart:
            ids.append(prod['id'])
        prods = Product.objects.filter(id__in=ids)
        for prod in prods:
            p = prod.toCart()
            for x in cart:
                if p['id'] == x['id']:
                    p['count'] = x['count']
            ret.append(p)
    return {
        'url_bits': request.path.split('/'),
        'all_categories': Category.objects.all().order_by('sort'),
        'cart_data': json.dumps(ret)
    }

def top_menu(request):
    top_menu = [
        {'name': 'О глютене', 'url': '/about/'},
        {'name': 'Рецепты', 'url': '/recipes/'},
        {'name': 'Целиакия и симптомы', 'url': '/celiac/'},
        {'name': 'Доставка и оплата', 'url': '/shipping/'},
        {'name': 'Контакты', 'url': '/contacts/'}
    ]
    return {'top_menu': top_menu}


def left_recipes(request):
    return {
        'left_recipes': Recipe.objects.filter(always_show=True)[:1]
    }