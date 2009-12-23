from django.conf.urls.defaults import *
from tekblog.models import Entry
from datetime import datetime

blog_dict = {
    'queryset': Entry.objects.filter(status=2, published_on__lte=datetime.now),
}

urlpatterns = patterns('',
    (r'^(?P<blog_slug>\w+)/$', 'tekblog.views.index', blog_dict),
    (r'^(?P<blog_slug>\w+)/(?P<slug>\w+)/$', 'tekblog.views.detail', blog_dict),
)

