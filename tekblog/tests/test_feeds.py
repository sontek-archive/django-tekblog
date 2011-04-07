from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from mock import patch, Mock

from tekblog.feeds import LatestEntriesFeed, TopicFeed
from tekblog.models import Entry

class LatestEntriesFeedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.user.save()

        entry1 = Entry(owner=self.user, title='Python and Django',
                draft=True, tags='python, django', markup=None)

        entry2 = Entry(owner=self.user, title='Django', draft=False,
                tags='python, django', content='foo bar\nbaz',
                markup='LinebreaksFormatter')

        entry1.save()
        entry2.save()

        entry1.sites = entry2.sites = Site.objects.all()

        entry1.save()
        entry2.save()


    @patch('tekblog.models.Entry.objects.active')
    def test_items(self, active_method):
        """
        Tests that the basic functionality of active feeds is used.
        """
        feed = LatestEntriesFeed()
        feed.items()
        active_method.assert_called_with()

    def test_only_active_entries_are_pulled(self):
        feed = LatestEntriesFeed()
        items = feed.items()
        self.assertEqual(len(items), 1)

    def test_pulls_correct_title(self):
        feed = LatestEntriesFeed()
        items = feed.items()
        item_title = feed.item_title(items[0])
        self.assertEqual(item_title, 'Django')

    def test_pulls_html_content(self):
        feed = LatestEntriesFeed()
        items = feed.items()
        item_content = feed.item_description(items[0])
        self.assertEqual(item_content, 'foo bar<br />baz')


class FeedItem(Mock):
    def __init__(self, title, html_content):
        self.title_mock = Mock(return_value=title)
        self.html_content_mock = Mock(return_value=html_content)

    @property
    def title(self):
        return self.title_mock()

    @property
    def html_content(self):
        return self.html_content_mock()

class TopicFeedTest(TestCase):
    @patch('tagging.models.TaggedItem.objects.get_by_model')
    def test_items(self, get_by_model_method):
        """
        Tests that the primary topic feed functions appropriately with
        the topic and active feed entries being used.
        """
        with patch('tekblog.models.Entry.objects.active') as active_call:
            results = Mock()
            active_call.side_effect = lambda *a, **k: results

            # Setup the return values so we have something to work with
            topic = Mock()
            topic.name = "Hello world"

            feed = TopicFeed()
            feed.items(topic)

            get_by_model_method.assert_called_with(results, '"%s"' % topic.name)
            active_call.assert_called_with()

    @patch('tagging.models.Tag.objects.get')
    def test_get_object(self, tag_get):
        topic = "Hello world"
        request = Mock()

        feed = TopicFeed()
        feed.get_object(request, topic)

        tag_get.assert_called_with(name=topic)

    def test_item_title(self):
        item = FeedItem('foo', 'baz')
        feed = TopicFeed()
        title = feed.item_title(item)
        self.assertEqual(title, 'foo')
        item.title_mock.assert_call_once_with()

    def test_item_description(self):
        item = FeedItem('foo', 'baz')
        feed = TopicFeed()
        description = feed.item_description(item)
        self.assertEqual(description, 'baz')
        item.html_content_mock.assert_call_once_with()
