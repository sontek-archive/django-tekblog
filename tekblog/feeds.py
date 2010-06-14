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
        return Entry.objects.active()
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.html_content
