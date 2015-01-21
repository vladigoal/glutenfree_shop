# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from unidecode import unidecode

from django.template.defaultfilters import slugify
from utils.slug import unique_slugify
from utils.image import get_resized_thumb

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(max_length=50, null=True, blank=True, verbose_name='url')
    sort = models.IntegerField(default=0, verbose_name='Сортировка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        app_label = 'product'

    def save(self, **kwargs):
        if not self.slug:
            self.slug = '%s' % (slugify(unidecode(u"%s"%self.name)))
            unique_slugify(self, self.slug)
        super(Category, self).save()


@python_2_unicode_compatible
class Brand(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(null=True, blank=True, upload_to='images/brands',
                              verbose_name='Лого')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'
        app_label = 'product'


def get_category():
    return Category.objects.get(id=1)

def get_brand():
    return Brand.objects.get(id=1)


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    slug = models.SlugField(max_length=50, null=True, blank=True, verbose_name='url')
    isActive = models.BooleanField(default=True, verbose_name='Активный')
    category = models.ForeignKey(Category, verbose_name='Категория')
    brand = models.ForeignKey(Brand, verbose_name='Бренд')
    soya_free = models.BooleanField(default=False,
                                     verbose_name = u'Без яиц')
    lactose_free = models.BooleanField(default=False,
                                     verbose_name = u'Без лактозы')
    kazein_free = models.BooleanField(default=False,
                                     verbose_name = u'Без казеина')
    soya_soya_free = models.BooleanField(default=False,
                                     verbose_name = u'Без сои')
    image = models.ImageField(null=True, blank=True,
                              upload_to='images/products',
                              verbose_name='Картинка')
    short_desc = models.TextField(verbose_name='Короткое описание')
    description = models.TextField(verbose_name='Длинное описание')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='Входящая цена')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name='Цена реализации')
    bulk = models.CharField(null=True, blank=True, max_length=30,
                            verbose_name='Вес/обьем')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = u'продукт'
        verbose_name_plural = u'продукты'
        app_label = 'product'

    def save(self, **kwargs):
        if not self.slug:
            self.slug = '%s' % (slugify(unidecode(u"%s"%self.name)))
            unique_slugify(self, self.slug)
        super(Product, self).save()

    def toCart(self):
        try:
            image = get_resized_thumb(self.image, '43x41')
        except:
            image = ""
        return {
            'id': self.id,
            'name': self.name,
            'pr': float(self.sell_price),
            'image': image,
            'count': 1
        }


@python_2_unicode_compatible
class Recipe(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    slug = models.SlugField(max_length=50, null=True, blank=True, verbose_name='url')
    always_show = models.BooleanField(default=False,
                                     verbose_name = u'Показывать слева')
    image = models.ImageField(null=True, blank=True,
                              upload_to='images/recipes',
                              verbose_name='Картинка')
    product = models.ManyToManyField(Product, verbose_name='Продукты')
    short_desc = models.TextField(verbose_name='Короткое описание')
    ingredients = models.TextField(verbose_name='Ингредиенты')
    cooking = models.TextField(verbose_name='Приготовление')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'рецепт'
        verbose_name_plural = u'рецепты'
        app_label = 'product'

    def save(self, **kwargs):
        if not self.slug:
            self.slug = '%s' % (slugify(unidecode(u"%s"%self.name)))
            unique_slugify(self, self.slug)
        super(Recipe, self).save()
