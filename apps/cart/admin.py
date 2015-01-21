# -*- coding: utf-8 -*-
from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from .models import CartProducts, Cart
from .export_cart import exportCartAdmin


class CartProductsInline(admin.StackedInline):
    model = CartProducts
    fieldsets = (
        (None, {
            'fields': ('cart', ('product', 'sell_price', 'count'))
        }),
    )
    verbose_name_plural = 'Товары'
    verbose_name = 'Продукт'
    extra = 0

class CartAdmin(exportCartAdmin):
    inlines = (CartProductsInline, )
    readonly_fields = ('total', 'total_price', 'total_price_discount')
    list_filter = ('status', ('tm_created', DateRangeFilter))
    list_display = ('name', 'phone', 'email', 'address', 'status', 'tm_created', 'total', 'total_price', 'discount', 'total_price_discount')

    def total(self, item):
        count = 0
        prods = CartProducts.objects.filter(cart=item.id)
        for prod in prods:
            count = count+prod.count
        return count

    total.short_description = u'Кол-во'

    def total_price(self, item):
        price = 0
        prods = CartProducts.objects.filter(cart=item.id)
        for prod in prods:
            price = price+(prod.sell_price * prod.count)
        return price
    total_price.short_description = u'На сумму'

    def total_price_discount(self, item):
        return self.total_price(item) - item.discount
    total_price_discount.short_description = u'Сумма со скидкой'

    class Media:
        css = {
            'all': ('/static/css/admin/cart.css',)
        }
        js = [
            '/static/js/admin/cart.js',
        ]

admin.site.register(Cart, CartAdmin)
# admin.site.register(CartProducts)
