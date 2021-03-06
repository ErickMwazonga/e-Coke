"""Coke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views as flat_views

from blogs.feeds import LatestBlogsFeed

from blogs.views import reward_blog


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('ecoke.urls')),
    url(r'^api/brands/', include('api.urls')),
    url(r'^blog/', include('blogs.urls')),

    # flatpages
    url(r'^eula/$', flat_views.flatpage, {'url': '/eula/'}, name='eula'),

    # Redactor WYSIWYG editor
    url(r'^redactor/', include('redactor.urls')),

    # RSS feeds.
    url(r'^latest/feed/$', LatestBlogsFeed(), name='rss_feed'),
    url(r'^reward_blog/$', reward_blog, name='reward_blog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
