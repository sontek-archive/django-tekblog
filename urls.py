from django.conf.urls.defaults import *
from tekblog.models import Entry
from datetime import datetime

blog_dict = {
    'queryset': Entry.active_objects,
}

urlpatterns = patterns('',
    # defaults to english
    (r'^(?P<blog_slug>[^/]+)/$', 'tekblog.views.entry_list', blog_dict),
    (r'^(?P<blog_slug>[^/]+)/(?P<slug>[^/]+)/$', 'tekblog.views.entry_detail', blog_dict),
    # allow defining the language a user wants to see
    (r'^(?P<blog_slug>[^/]+)/(?P<locale>\w+)/$', 'tekblog.views.entry_list', blog_dict),
    (r'^(?P<blog_slug>[^/]+)/(?P<locale>\w+)/(?P<slug>[^/]+)/$', 'tekblog.views.entry_detail', blog_dict),
)

