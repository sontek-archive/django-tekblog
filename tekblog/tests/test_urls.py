from django.test import TestCase
from django.contrib.auth.models import User
from tekblog.models import Entry

from django.test.client import Client

#        url(r'^$', index, name='tekblog_index'),
#        url(r'^topic/(?P<topic>[^/]*)/?$', index, name='tekblog_index'),
#        url(r'^search/$', search, name='tekblog_search'),
#        url(r'^(?P<page>\d*)/?$', index, name='tekblog_index'),
#        url(r'^(?P<slug>[^/]*)/?$', detail, name='tekblog_detail'),

class SimpleUrlViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create(username='user1', is_staff=True)
        self.staff_user.set_password('test')
        self.staff_user.save()

        self.entry1 = Entry(owner=self.staff_user, title='Python and Django',
                draft=True, tags='python, django, bleh', markup=None)
        self.entry1.save()

    def test_index(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)

    def test_index_topic(self):
        response = self.client.get('/topic/bleh/')
        self.assertEquals(200, response.status_code)
