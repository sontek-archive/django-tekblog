from django.conf.urls.defaults import *
from blog.models import Entry
from datetime import datetime

blog_dict = {
    'queryset': Entry.objects.filter(status=2, published_on__lte=datetime.now),
}

urlpatterns = patterns('',
    (r'^(?P<blog_slug>\w+)/$', 'blog.views.index', blog_dict),
    (r'^(?P<blog_slug>\w+)/(?P<slug>\w+)/$', 'blog.views.detail', blog_dict),
)

