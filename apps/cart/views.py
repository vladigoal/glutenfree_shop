# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.utils import simplejson as json
import urllib
from apps.product.models import Product
from .models import Cart, CartProducts
from django.http import HttpResponse, HttpResponseRedirect
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
import cStringIO as StringIO
import datetime
from django.conf import settings
import os
from django.core.mail import send_mail


class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated and not self.request.user.is_anonymous():
            try:
                phone = self.request.user.shopuser.phone
            except:
                phone = ''
            context['user_data'] = json.dumps({
                'name': self.request.user.last_name + " " + self.request.user.first_name,
                'email': self.request.user.email,
                'phone': phone
            })
        return context


class NewOrder(View):

    def post(self, request, *args, **kwargs):
        user = None
        if 'user_id' in self.request.POST:
            user = User.objects.get(id=int(self.request.POST['user_id']))

        new_order = Cart(
            address = self.request.POST['adress'],
            phone = self.request.POST['phone'],
            email = self.request.POST.get('email'),
            user = user,
            discount = 0,
            name = self.request.POST['fio']
        )
        new_order.save()
        
        sum = 0
        prod = ''
        for p in self.request.POST['prod'].rsplit(','):
            if len(p):
                t = p.rsplit(':')
                product = Product.objects.filter(id=int(t[0]))
                if product:
                    add_prod = CartProducts(
                        product = product[0],
                        cart = new_order,
                        sell_price = product[0].sell_price,
                        count = int(t[1])
                    )
                    prod = prod + u'%s: %s грн. x %s шт - %s грн. \n'%(product[0].name, product[0].sell_price, t[1], (product[0].sell_price *  int(t[1])))
                    sum = sum + (product[0].sell_price *  int(t[1]))                    
                    add_prod.save()

        if self.request.POST.get('email'):
            msg = u'Здравствуйте! \n'
            msg = msg + u'В магазине "GlutenOFF.COM.UA" Вы заказали \n'
            msg = msg + prod + '\n'
            msg = msg + u'На сумму: %s грн \n \n'%sum
            msg = msg + u'Для подтверждения заказа наш менеджер свяжется с Вами в ближайшее время! \n'
            msg = msg + u'До новых встреч в нашем магазине!'

            send_mail('GlutenOFF.COM.UA', msg, 'office@glutenoff.com.ua', [self.request.POST['email']], fail_silently=False)

        msg = u'Новый заказ от %s \n'%self.request.POST.get('fio')
        msg = msg + u'Телефон: %s \n'%self.request.POST['phone']
        msg = msg + u'Email: %s \n'%self.request.POST.get('email')
        msg = msg + u'Адрес доставки: %s \n'%self.request.POST['adress']
        msg = msg + prod + '\n'
        msg = msg + u'На сумму: %s грн. \n \n'%sum

        send_mail('GlutenOFF.COM.UA', msg, 'office@glutenoff.com.ua', ['mc@muravied.com', 'office@muravied.com'], fail_silently=False)
        return HttpResponse(
            json.dumps({'res': 'ok'}),
            mimetype="application/json" )


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def print_order_view(request):
    try:
        orders = request.GET['orders']
    except:
        orders = None

    orders_ids = []
    for o in orders.split(','):
        if o:
            orders_ids.append(int(unicode.encode(o)))
    cart = []
    for ca in Cart.objects.filter(id__in=orders_ids):
        order_products = CartProducts.objects.filter(cart=ca.id)
        total_price = 0
        for cart_product in order_products:
            total_price += cart_product.count * cart_product.sell_price

        cart.append({
            'order': ca,
            'order_products': order_products,
            'total_price': total_price,
            'total_price_discount': total_price - ca.discount,
        })
    return render_to_pdf(
        'print_order.html',
        {
            'pagesize':'A4',
            'carts': cart,
            'now': datetime.datetime.now(),
            'font_path': os.path.join(settings.BASE_DIR, settings.PROJECT_NAME, 'static', 'fonts')
        }
    )