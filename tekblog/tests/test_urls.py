from unittest import TestCase

from django.test.client import Client

#        url(r'^$', index, name='tekblog_index'),
#        url(r'^topic/(?P<topic>[^/]*)/?$', index, name='tekblog_index'),
#        url(r'^search/$', search, name='tekblog_search'),
#        url(r'^(?P<page>\d*)/?$', index, name='tekblog_index'),
#        url(r'^(?P<slug>[^/]*)/?$', detail, name='tekblog_detail'),

class SimpleUrlViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)

    def test_index_topic(self):
        response = self.client.get('topic/bleh/')
        self.assertEquals(200, response.status_code)
