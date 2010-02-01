from django.conf.urls.defaults import *
from datetime import datetime
from tekblog.views import index, detail

urlpatterns = patterns('tekblog.views',
        url(r'^$', index, name='tekblog_index'),
        url(r'^(?P<slug>[^/]+)$', detail, name='tekblog_detail'),
)

