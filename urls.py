from django.conf.urls.defaults import *
from tekblog.models import Entry
from datetime import datetime

blog_dict = {
    'queryset': Entry.active_objects,
}

urlpatterns = patterns('',
    # defaults to english
    (r'^(?P<blog_slug>\w+)/$', 'tekblog.views.entry_list', blog_dict),
    (r'^(?P<blog_slug>\w+)/(?P<slug>\w+)/$', 'tekblog.views.entry_detail', blog_dict),
    # allow defining the language a user wants to see
    (r'^(?P<blog_slug>\w+)/(?P<locale>\w+)/$', 'tekblog.views.entry_list', blog_dict),
    (r'^(?P<blog_slug>\w+)/(?P<locale>\w+)/(?P<slug>\w+)/$', 'tekblog.views.entry_detail', blog_dict),
)

