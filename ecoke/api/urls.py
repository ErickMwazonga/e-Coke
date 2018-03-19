# django imports
from django.conf.urls import url, include
from django.contrib import admin
# DRF imports
from rest_framework.authtoken.views import obtain_auth_token
#  App imports
from . import views
from .views import (
    BrandCreateAPIView,
    BrandListAPIView,
    BrandRetrieveAPIView,
    BrandUpdateAPIView,
    BrandDeleteAPIView,
    BrandDetailsView,
)

app_name = 'api_brands'

urlpatterns = [
    url(r'^create$', BrandCreateAPIView.as_view(), name="create"),
    url(r'^$', BrandListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', BrandRetrieveAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', BrandUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', BrandDeleteAPIView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/details$', BrandDetailsView.as_view(), name="details"),

    # Browsable API
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^get-token/', obtain_auth_token),
]
