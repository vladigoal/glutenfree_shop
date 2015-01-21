from django.contrib import admin
from apps.product.models import Category, Product, Brand, Recipe

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'soya_free', 'lactose_free')
    list_filter = ["soya_free", 'lactose_free']
    search_fields = ['name',]

    class Media:
        js = [
             '/static/libs/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
             '/static/libs/grappelli/tinymce_setup/tinymce_setup.js',
        ]

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Media:
        js = [
             '/static/libs/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
             '/static/libs/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Recipe, RecipeAdmin)