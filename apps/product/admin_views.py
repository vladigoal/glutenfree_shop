# -*- coding: utf-8 -*-
from .models import Product
from django.http import HttpResponse
import json

def get_product(request):
    product_id = request.GET['product_id']

    cart_product = Product.objects.filter(id=product_id)
    if cart_product:
        return HttpResponse(json.dumps({'price': str(cart_product[0].sell_price)}), mimetype="application/json" )
    else:
        return HttpResponse(json.dumps({'price': ''}), mimetype="application/json" )

