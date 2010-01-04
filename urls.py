from django.conf.urls.defaults import *
from tekblog.models import Entry
from datetime import datetime

blog_dict = {
    'queryset': Entry.active_objects,
}

urlpatterns = patterns('tekblog.views',
    url(r'^(?P<blog_slug>[^/]+)/$', 'entry_list', blog_dict, name='entry_list'),
    url(r'^(?P<blog_slug>[^/]+)/(?P<slug>[^/]+)/$', 'entry_detail', blog_dict, name='entry_detail'),
)

