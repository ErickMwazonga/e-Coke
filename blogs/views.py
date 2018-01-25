from django.views.generic.base import ContextMixin
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, JsonResponse

from taggit.models import TaggedItem

from .models import Blog, BlogAd


class BlogBaseView(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(BlogBaseView, self).get_context_data(**kwargs)
        context['blog_tags'] = TaggedItem.tags_for(Blog).order_by('name')
        context['recent_blog_list'] = Blog.objects.recent_posts()
        # context['blog_list'] = Blog.objects.all()

        return context


class BlogDetailView(DetailView, BlogBaseView):
    model = Blog

    def get_queryset(self):
        """
        Only return the object if it's public, unless the user is a superuser.
        """
        if self.request.user.is_authenticated() and \
                self.request.user.is_superuser:
            return Blog.objects.all()
        else:
            return Blog.objects.publicly_viewable()

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        # To order randomly, use "?", like so, but it may be slow
        context['add_top'] = BlogAd.objects.filter(position=BlogAd.TOP).order_by('?').first()
        context['add_middle'] = BlogAd.objects.filter(position=BlogAd.MIDDLE).order_by('?').first()
        context['add_bottom'] = BlogAd.objects.filter(position=BlogAd.BOTTOM).order_by('?').first()

        return context


class BlogListView(ListView, BlogBaseView):
    model = Blog
    pagiante_by = 15
    context_object_name = 'blog_list'
    template_name = 'blogs/blog_list.html'

    def get_queryset(self):
        """
        Only return public blog posts.
        """
        # blogs = [Blog.objects.filter(author=self.request.user).all()]
        # if blog.user == self.request.user:
        if self.request.user.is_authenticated() and \
                self.request.user.is_superuser:
            return Blog.objects.all()
        else:
            return Blog.objects.publicly_viewable()


class BlogTagListView(BlogListView):
    """
    Display a Blog List Page filtered by tag,
    """

    def get_queryset(self):
        result = super(BlogTagListView, self).get_queryset()
        return result.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super(BlogTagListView, self).get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag')

        return context


class BlogAuthorListView(BlogListView):
    """
    Display a Blog List Page filtered by author,
    """
    slug_field = "username"

    def get_queryset(self):
        result = super(BlogAuthorListView, self).get_queryset()
        # print(self.kwargs.get('username'))
        return result.filter(author__username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super(BlogAuthorListView, self).get_context_data(**kwargs)
        context['author_name'] = self.kwargs.get('username')

        return context


def reward_blog(request):
    # if request.method == 'POST':
    blog_id = request.POST.get('blog_id', None)

    rewards = 0
    if (blog_id):
        blog = Blog.objects.get(id=int(blog_id))
        if blog is not None:
            rewards = blog.rewards + 1
            blog.rewards = rewards
            blog.save()

    return HttpResponse(rewards)
