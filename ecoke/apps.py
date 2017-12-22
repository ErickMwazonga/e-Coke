# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class EcokeConfig(AppConfig):
    name = 'ecoke'

    def ready(self):
        from . import signals   # noqa
