from django.contrib import admin
from django.contrib.flatpages.models import FlatPage


class FlatPageAdmin(admin.ModelAdmin):
    # readonly_fields = ('url',)

    class Media:
        js = [
             '/static/libs/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
             '/static/libs/grappelli/tinymce_setup/tinymce_setup.js',
        ]


# Re-register UserAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
