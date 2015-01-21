# -*- coding: utf-8 -*-
import os
from sorl.thumbnail.shortcuts import get_thumbnail
from django.conf import settings

def get_resized_thumb(image, size, image_folder='', crop='center'):
    if image:
        res_image = get_thumbnail(os.path.join(settings.MEDIA_ROOT, image_folder, image.name), size, crop=crop)
        return res_image.url
    else:
        return 'http://placehold.it/43x41/f3ede1&text=NO%20PHOTO'