from django.conf.urls.defaults import *
from datetime import datetime
from tekblog.views import index, detail, search
from tekblog.feeds import LatestEntriesFeed, TopicFeed

urlpatterns = patterns('tekblog.views',
        url(r'^$', index, name='tekblog_index'),
        url(r'^topic/(?P<topic>[^/]*)/?$', index, name='tekblog_index'),
        url(r'^search/$', search, name='tekblog_search'),
        url(r'^(?P<page>\d*)/?$', index, name='tekblog_index'),
        url(r'^(?P<slug>[^/]*)/?$', detail, name='tekblog_detail'),
        # support blogengine.net url's
        url(r'^post/(?P<slug>[^/]*).aspx$', detail, name='tekblog_detail_be'),
        (r'^comments/', include('django.contrib.comments.urls')),
        (r'^feeds/latest/$', LatestEntriesFeed()),
        (r'^feeds/(?P<topic>[^/]*)/$', TopicFeed()),
)
