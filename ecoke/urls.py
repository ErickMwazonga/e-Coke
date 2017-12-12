from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.edit import CreateView

from . import views
from .forms import UserCreateForm
from .views import IndexView, BrandListView, LoginView

app_name = 'ecoke'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^brand$', views.brand_create, name="brand_create"),
    url(r'^brand/(?P<pk>\d+)/update/$', views.brand_update, name='brand_update'),
    url(r'^brand/(?P<pk>\d+)/delete/$', views.brand_delete, name='brand_delete'),
    url(r'^brands$', BrandListView.as_view(), name='brands'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url('^register/', CreateView.as_view(
            template_name='ecoke/register.html',
            form_class=UserCreateForm,
            success_url='/login'
    ),
        name='register'
    ),
    url(r'^logout/$', auth_views.logout_then_login, {'login_url': 'ecoke:login'}, name='logout'),
    url(r'^settings/edit-profile$', views.edit_profile, name='edit_profile'),
    url(r'^settings/change-password/$', views.change_password, name='change_password'),

    url(r'^brand/csv$', views.export_csv, name="export_csv"),
]
