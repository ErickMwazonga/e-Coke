from django.conf.urls import url

from .views import BlogDetailView, BlogListView, BlogTagListView, BlogAuthorListView

from . import views

app_name = 'blogs'

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list_view',),
    url(r'^tag/(?P<tag>[\w ]+)/$', BlogTagListView.as_view(), name='blog_tag_list_view',),
    url(r'^by/(?P<username>[\w-]+)/$', BlogAuthorListView.as_view(), name='blog_author_list_view',),
    url(r'^(?P<slug>[\w-]+)/$', BlogDetailView.as_view(), name='blog_detail_view',),
    # url(r'^reward_blog/$', views.reward_blog, name='reward_blog'),
]
