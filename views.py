from tekblog.models import Blog, Entry
from django.views.generic.list_detail import object_list, object_detail

def entry_list(request, blog_slug):
    """ The list of entries """
    blog = Blog.objects.filter(slug=blog_slug)
    entries = Entry.active_objects.filter(blog=blog)
    return object_list(request, queryset=entries)
    
def entry_detail(request, blog_slug, slug, queryset):
    """ The permalink/detail view of an entry """
    blog = Blog.objects.filter(slug=blog_slug)
    entries = Entry.active_objects.filter(blog=blog)
    return object_detail(request, slug=slug, queryset=entries)
