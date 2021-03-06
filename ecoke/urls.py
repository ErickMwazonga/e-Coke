from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from .views import IndexView, BrandListView, LoginView, FeedbackFormView

app_name = 'ecoke'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^brand$', views.brand_create, name="brand_create"),
    url(r'^brand/(?P<pk>\d+)/update/$', views.brand_update, name='brand_update'),
    url(r'^brand/(?P<pk>\d+)/delete/$', views.brand_delete, name='brand_delete'),
    url(r'^brands$', BrandListView.as_view(), name='brands'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url('^register/', views.register, name='register'),
    url(r'^activate/account/$', views.activate_account, name='activate'),
    url(r'^logout/$', auth_views.logout_then_login, {'login_url': 'ecoke:login'}, name='logout'),
    url(r'^settings/edit-profile$', views.edit_profile, name='edit_profile'),
    url(r'^settings/change-password/$', views.change_password, name='change_password'),
    url(r'^settings/profile/(?P<slug>[\w-]+)/$', views.ProfileDetailView.as_view(), name='profile'),

    url(r'^feedback/$', FeedbackFormView.as_view(), name='feedback'),
    url(r'^feedback/(?P<username>[\w-]+)/$', login_required(FeedbackFormView.as_view()), name='feedback'),

    url(r'^brand/csv$', views.export_csv, name="export_csv"),
]
