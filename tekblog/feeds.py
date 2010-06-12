from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from tekblog.models import Entry, Series

class LatestEntriesFeed(Feed):
    _site = Site.objects.get_current()
    link = '/'
    title = '%s feed' % _site.name
    description = '%s latest posts feed.' % _site.name

    def items(self):
        import pdb
        pdb.set_trace()
        return Entry.objects.active()
