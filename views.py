from blog.models import Blog
from django.views.generic.list_detail import object_list, object_detail

def index(request, blog_slug, queryset, **kwargs):
    blog = Blog.objects.filter(slug=blog_slug)
    entries = queryset.filter(blog=blog)
    return object_list(request, queryset=entries, **kwargs)
    
def detail(request, blog_slug, slug, queryset, **kwargs):
    blog = Blog.objects.filter(slug=blog_slug)
    entries = queryset.filter(blog=blog)
    return object_detail(request, slug=slug, queryset=entries, **kwargs)
