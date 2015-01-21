# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from .models import Product, Category, Recipe
from django.utils import simplejson as json
from utils.image import get_resized_thumb


def build_catalog_products(products, img_size):
    try:
        image = get_resized_thumb(item.image, img_size)
    except:
        image = ""
    return [
        {
            'name': item.name,
            'isActive': item.isActive,
            'description': item.description,
            'pr': item.sell_price,
            'image': item.image,
            'bulk': item.bulk,
            'slug': item.slug,
            'json': json.dumps({
                'id': item.id,
                'name': item.name,
                'bulk': item.bulk,
                'image': image,
                'pr': str(item.sell_price),
                'count': 1
            })
        }
        for item in products]

class CatalogView(TemplateView):
    template_name = "catalog.html"

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)
        if self.request.get_full_path() == "/":
            context['catalog'] = build_catalog_products(Product.objects.filter(isActive=True), '43x41')[:12]
        else:
            context['catalog'] = build_catalog_products(Product.objects.filter(isActive=True).filter(**self.filter_params()), '43x41')
        return context

    def filter_params(self):
        filter_dict = {}
        if self.request.GET:
            for key, val in self.request.GET.iteritems():
                if key == 'searchword':
                    filter_dict['name__icontains'] = self.request.GET['searchword']
                if key == 'sort':
                    if self.request.GET['sort'] == 'popular':
                        pass
                    if self.request.GET['sort'] == 'soya_free':
                        filter_dict['soya_free'] = True
                    if self.request.GET['sort'] == 'lactose_free':
                        filter_dict['lactose_free'] = True
                    if self.request.GET['sort'] == 'kazein_free':
                        filter_dict['kazein_free'] = True
                    if self.request.GET['sort'] == 'soya_soya_free':
                        filter_dict['soya_soya_free'] = True

        return filter_dict


class CategoryView(TemplateView):
    template_name = "catalog.html"

    def get_context_data(self, **kwargs):
        path = self.request.path.split('/')
        if len(path) > 2:
            if path[2]:
                category_slug = path[2]
        else:
            category_slug = None

        context = super(CategoryView, self).get_context_data(**kwargs)
        if category_slug:
            categories_ids = [item.id for item in Category.objects.filter(slug=category_slug)]
            products = Product.objects.filter(category_id__in=categories_ids, isActive=True)
            context['catalog'] = build_catalog_products(products, '43x41')
        return context


class ProductView(TemplateView):
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        path = self.request.path.split('/')
        if len(path) > 2:
            if path[2]:
                slug = path[2]
        else:
            slug = None

        context = super(ProductView, self).get_context_data(**kwargs)
        if slug:
            context['product'] = build_catalog_products(Product.objects.filter(slug=slug), '260')
        print context['product'][0]
        return context

class RecipesView(TemplateView):


    def recipes(request):
        return Recipe.objects.all()    

    template_name = "recipes.html"

class RecipeView(TemplateView):
    template_name = "recipe.html"

    def get_context_data(self, **kwargs):
        path = self.request.path.split('/')
        if len(path) > 2:
            if path[2]:
                slug = path[2]
        else:
            slug = None

        context = super(RecipeView, self).get_context_data(**kwargs)
        if slug:
            recipes = Recipe.objects.filter(slug=slug)
            context['recipe'] = recipes
            relative_products = recipes[0].product.all()
            context['relative_products'] = build_catalog_products(relative_products, '154')
            if recipes:
                try:
                    image = get_resized_thumb(item.image, '43x41')
                except:
                    image = ""
                buy_full_recipe_json = [{
                    'id': item.id,
                    'name': item.name,
                    'bulk': item.bulk,
                    'image': image,
                    'sell_price': str(item.sell_price),
                    'count': 1
                } for item in relative_products]
                context['buy_full_recipe_json'] = json.dumps(buy_full_recipe_json)
        return context


