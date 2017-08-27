# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Brand

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    '''
    Customizing the Brand Admin Dashboard
    '''
    list_display  = ('collector_name', 'respondent_name', 'respondent_city')
    search_fields = ('collector_name', 'respondent_name', 'respondent_city')
    list_filter   = ('date_of_collection',)
    ordering      = ('-date_of_collection',)

admin.site.register(Brand, BrandAdmin)
