# django imports
from django.conf.urls import url
from django.contrib import admin
#  App imports
from . import views
from .views import (
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,
    UserLoginAPIView,
)

app_name = 'api_users'

urlpatterns = [
    url(r'^register$', UserCreateAPIView.as_view(), name="register"),
    url(r'^login$', UserLoginAPIView.as_view(), name="login"),
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', UserRetrieveAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', UserUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', UserDeleteAPIView.as_view(), name='delete'),
]
