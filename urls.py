from django.conf.urls.defaults import *
from tekblog.models import Entry
from datetime import datetime

active_entries = {
    'queryset': Entry.active_objects.all(),
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', active_entries, name='entry_list'),
    url(r'^(?P<slug>[^/]+)/$', 'object_detail', active_entries, name='entry_detail'),
)

