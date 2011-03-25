from unittest import TestCase
from mock import patch, Mock

from tekblog.feeds import LatestEntriesFeed, TopicFeed

class LatestEntriesFeedTest(TestCase):
    """
    Tests that the basic functionality of active feeds is used.
    """
    @patch('tekblog.models.Entry.objects.active')
    def test_items(self, active_method):
        feed = LatestEntriesFeed()
        feed.items()
        active_method.assert_called_with()


class TopicFeedTest(TestCase):
    """
    Tests that the primary topic feed functions appropriately with
    the topic and active feed entries being used.
    """
    @patch('tagging.models.TaggedItem.objects.get_by_model')
    def test_items(self, get_by_model_method):
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
