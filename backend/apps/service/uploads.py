# -*- coding: utf-8 -*-
import os

from django.conf import settings

PHOTO_MEDIA_PATH = getattr(settings, 'PHOTO_MEDIA_PATH', 'photos')


def gen_file_path(instance, file_name, bound_getter, relative_path):
    bound = bound_getter(instance) or 'all'
    return os.path.join(relative_path, f'{bound}', file_name)


def photo_uploads(instance, file_name):
    return gen_file_path(
        instance,
        file_name,
        lambda el: el.todo and el.todo.id or None,
        PHOTO_MEDIA_PATH
    )
