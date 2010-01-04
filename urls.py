from django.conf.urls.defaults import *
from tekblog.models import Entry
from datetime import datetime

blog_dict = {
    'queryset': Entry.active_objects,
}

urlpatterns = patterns('tekblog.views',
    # defaults to english
    (r'^(?P<blog_slug>[^/]+)/$', 'entry_list', blog_dict),
    (r'^(?P<blog_slug>[^/]+)/(?P<slug>[^/]+)/$', 'entry_detail', blog_dict),
    # allow defining the language a user wants to see
    (r'^(?P<blog_slug>[^/]+)/(?P<locale>\w+)/$', 'entry_list', blog_dict),
    url(r'^(?P<blog_slug>[^/]+)/(?P<locale>\w+)/(?P<slug>[^/]+)/$', 'entry_detail', blog_dict, name="entry_detail"),
)

