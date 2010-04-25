from django.conf.urls.defaults import *
from datetime import datetime
from tekblog.views import index, detail

urlpatterns = patterns('tekblog.views',
        url(r'^$', index, name='tekblog_index'),
        url(r'^(?P<page>\d*)/?$', index, name='tekblog_index'),
        url(r'^(?P<slug>[-\w\(\)]+)/?$', detail, name='tekblog_detail'),
        # support blogengine.net url's
        url(r'^post/(?P<slug>[-\w\(\)]+).aspx$', detail, name='tekblog_detail_be'),
        (r'^comments/', include('django.contrib.comments.urls')),
)
