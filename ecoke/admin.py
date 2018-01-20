# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Brand, Feedback, Profile


# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    '''
    Customizing the Brand Admin Dashboard
    '''
    list_display = ('collector_name', 'respondent_name', 'respondent_city', 'created_at', 'updated_at')
    search_fields = ('collector_name', 'respondent_name', 'respondent_city',  'created_at', 'updated_at')
    list_filter = ('date_of_collection',)
    ordering = ('-date_of_collection',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    '''
    Customizing the Brand Admin Dashboard
    '''
    list_display = ('name', 'email', 'msg_short_description', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'message',  'created_at', 'updated_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''
    Customizing the Brand Admin Dashboard
    '''
    list_display = ('user', 'bio', 'location', 'job_title', 'avatar', 'created_at', 'updated_at')
    search_fields = ('user', 'bio', 'location', 'job_title', 'avatar',  'created_at', 'updated_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
