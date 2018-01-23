from datetime import datetime

from django.contrib import admin
from django import forms

from redactor.widgets import RedactorEditor

from .models import Blog, BlogAd


# Register your models here.
class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        widgets = {
           'content': RedactorEditor(),
        }
        exclude = ('created_at', 'updated_at')
        # fields = ('status', 'author', 'title', 'slug', 'content', 'tags', 'date_published')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm

    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('title', 'author', 'status', 'date_published', 'created_at',
                    'updated_at', 'tag_list',)
    list_select_related = ('author',)
    list_filter = ('status', 'author', 'tags',)
    search_fields = ('title', 'content',)
    fieldsets = (
        ('', {
            'fields': ('status', 'author')
        }),
        ('Content', {
            'fields': ('title', 'slug', 'content', 'tags', 'date_published')
        }),
    )

    def tag_list(self, obj):
        """
        Retrieve the tags separated by comma,
        """
        return ','.join([t.name for t in obj.tags.all()])

    tag_list.short_description = 'Tags'

    def get_form(self, request, obj=None, **kwargs):
        """
        Set default author based on logged in user.
        """
        form = super(BlogAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user

        return form

    def save_model(self, request, obj, form, change):
        """
        Automatically set the published_date if the value is None
        and the status is set to 'published'.
        """
        if not obj.date_published and obj.status == 'published':
            obj.date_published = datetime.now()

        super(BlogAdmin, self).save_model(request, obj, form, change)


@admin.register(BlogAd)
class BlogAdAdmin(admin.ModelAdmin):
    list_display = ('description', 'position', 'created_at', 'updated_at')
