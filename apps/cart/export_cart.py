# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from import_export import admin as ie_admin
from import_export import resources
from import_export import fields
from import_export import widgets
from import_export.formats import base_formats
from import_export.forms import ExportForm
from .models import Cart, CartProducts

import sys
if sys.version_info[0] > 2:
    from io import BytesIO
    import tablib.packages.xlwt3 as xlwt
    
else:
    from cStringIO import StringIO as BytesIO
    import tablib.packages.xlwt as xlwt


class CartResource(resources.ModelResource):
    fio                     = fields.Field(column_name='ФИО',               widget=widgets.CharWidget(),    attribute='name')
    phone                   = fields.Field(column_name='Телефон',           widget=widgets.CharWidget(),    attribute='phone')
    email                   = fields.Field(column_name='e-mail',            widget=widgets.CharWidget(),    attribute='email')
    address                 = fields.Field(column_name='Адрес доставки',    widget=widgets.CharWidget(),    attribute='address')
    status                  = fields.Field(column_name='Статус заказа',     widget=widgets.CharWidget()     )
    date                    = fields.Field(column_name='Дата заказа',       widget=widgets.DateWidget(),    attribute='tm_created')
    total                   = fields.Field(column_name='Кол-во товаров',    widget=widgets.IntegerWidget()  )
    total_price             = fields.Field(column_name='На сумму',          widget=widgets.NumberWidget()   )
    discount                = fields.Field(column_name='Скидка',            widget=widgets.NumberWidget(),  attribute='discount')
    total_price_discount    = fields.Field(column_name='Сумма со скидкой',  widget=widgets.NumberWidget()   )
    products                = fields.Field(column_name='Товары',            widget=widgets.CharWidget()     )

    class Meta:
        model = Cart
        exclude  = ('id',)
        export_order = ('fio', 'phone', 'email', 'address', 'status', 'date', 'total', 'total_price', 'discount', 'total_price_discount', 'products')


    def dehydrate_status(self, info):
        for i in Cart.status_arr:
            if i[0] == info.status:
                return i[1]
        return ""
    
    def dehydrate_total(self, item):
        count = 0
        prods = CartProducts.objects.filter(cart=item.id)
        for prod in prods:
            count = count+prod.count
        return count

    def dehydrate_total_price(self, item):
        price = 0
        prods = CartProducts.objects.filter(cart=item.id)
        for prod in prods:
            price = price+(prod.sell_price*prod.count)
        return price

    def dehydrate_total_price_discount(self, item):
        return self.dehydrate_total_price(item) - item.discount
    
    def dehydrate_products(self, item):
        res = []
        prods = CartProducts.objects.filter(cart=item.id)
        for prod in prods:
            res.append(u"%s | %s шт. | %s грн./шт." % (prod.product.name, prod.count, prod.sell_price))

        return "\n".join(res)


class XLS(base_formats.XLS):
    
    def export_data(self, dataset):
        wb = xlwt.Workbook(encoding='utf8')
        ws = wb.add_sheet(dataset.title if dataset.title else 'Tablib Dataset', cell_overwrite_ok=True)

        wb.default_style.font.height = 20 * 36
        
        ws.col(0).width = int(25*380)
        ws.col(1).width = int(11*380)
        ws.col(2).width = int(15*380)
        ws.col(3).width = int(25*380)
        ws.col(4).width = int(10*380)
        ws.col(5).width = int(9*380)
        ws.col(6).width = int(10*380)
        ws.col(7).width = int(7*380)
        ws.col(8).width = int(6*380)
        ws.col(9).width = int(10*380)
        ws.col(10).width = int(50*380)

        self.dset_sheet(dataset, ws)

        stream = BytesIO()
        wb.save(stream)
        return stream.getvalue()


    def dset_sheet(self, dataset, ws):
        wrap = xlwt.easyxf("alignment: wrap on; align: vert top;")
        allstyle = xlwt.easyxf("align: vert top;")
        bold = xlwt.easyxf("font: bold on")

        """Completes given worksheet from given Dataset."""
        _package = dataset._package(dicts=False)

        for i, sep in enumerate(dataset._separators):
            _offset = i
            _package.insert((sep[0] + _offset), (sep[1],))

        for i, row in enumerate(_package):
            for j, col in enumerate(row):

                # bold headers
                if (i == 0) and dataset.headers:
                    ws.write(i, j, col, bold)

                    # frozen header row
                    ws.panes_frozen = True
                    ws.horz_split_pos = 1


                # bold separators
                elif len(row) < dataset.width:
                    ws.write(i, j, col, bold)

                # wrap the rest
                else:
                    try:
                        if '\n' in col:
                            ws.write(i, j, col, wrap)
                        else:
                            ws.write(i, j, col, allstyle)
                    except TypeError:
                        ws.write(i, j, col, allstyle)




class exportCartAdmin(ie_admin.ImportExportModelAdmin):
    change_list_template = 'admin/import_export/change_list_export.html'
    resource_class = CartResource
    formats = (
        XLS,
    )

    def export_action(self, request, *args, **kwargs):
        formats = self.get_export_formats()
        form = ExportForm(formats, request.POST or None)
        if form.is_valid() or len(formats) == 1:
            if form.is_valid():
                file_format = formats[
                    int(form.cleaned_data['file_format'])
                ]()
            else:
                file_format = formats[0]()

            queryset = self.get_export_queryset(request)
            export_data = self.get_export_data(file_format, queryset)
            content_type = 'application/octet-stream'
            # Django 1.7 uses the content_type kwarg instead of mimetype
            try:
                response = HttpResponse(export_data, content_type=content_type)
            except TypeError:
                response = HttpResponse(export_data, mimetype=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                self.get_export_filename(file_format),
            )
            return response

        context = {}
        context['form'] = form
        context['opts'] = self.model._meta
        return TemplateResponse(request, [self.export_template_name],
                                context, current_app=self.admin_site.name)