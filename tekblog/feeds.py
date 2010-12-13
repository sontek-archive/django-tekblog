from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from tekblog.models import Entry, Series
from tagging.models import TaggedItem, Tag


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


class TopicFeed(LatestEntriesFeed):
    def get_object(self, request, topic):
        t = Tag.objects.get(name=topic)
        return t

    def items(self, topic):
        # need to do this so django-tagging will allow muliple words in a tag
        cleaned_topic = '"%s"' % (topic.name)
        active_entries = TaggedItem.objects.get_by_model(
                Entry.objects.active(), cleaned_topic)
        return active_entries

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.html_content
