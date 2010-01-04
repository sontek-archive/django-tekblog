from tekblog.models import Blog
from django.views.generic.list_detail import object_list, object_detail

def entry_list(request, blog_slug, queryset, locale="en", **kwargs):
    """ The list of entries """
    blog = Blog.objects.filter(slug=blog_slug)
    entries = queryset.filter(blog=blog, locale=locale)
    return object_list(request, queryset=entries, **kwargs)
    
def entry_detail(request, blog_slug, slug, queryset, locale="en", **kwargs):
    """ The permalink/detail view of an entry """
    blog = Blog.objects.filter(slug=blog_slug)
    entries = queryset.filter(blog=blog, locale=locale)
    return object_detail(request, slug=slug, queryset=entries, **kwargs)
