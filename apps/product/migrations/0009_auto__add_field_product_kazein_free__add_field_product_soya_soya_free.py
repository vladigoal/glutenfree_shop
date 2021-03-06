# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.kazein_free'
        db.add_column(u'product_product', 'kazein_free',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Product.soya_soya_free'
        db.add_column(u'product_product', 'soya_soya_free',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.kazein_free'
        db.delete_column(u'product_product', 'kazein_free')

        # Deleting field 'Product.soya_soya_free'
        db.delete_column(u'product_product', 'soya_soya_free')


    models = {
        u'product.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'product.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'product.product': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Brand']"}),
            'bulk': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'kazein_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lactose_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'purchase_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'sell_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'short_desc': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'soya_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'soya_soya_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'product.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'always_show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cooking': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'product': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.Product']", 'symmetrical': 'False'}),
            'short_desc': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['product']