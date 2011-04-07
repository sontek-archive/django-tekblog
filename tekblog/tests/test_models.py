from django.test import TestCase
from tekblog.models import Series, Entry
from django.contrib.auth.models import User

class ModelsTestCase(TestCase):
    def setUp(self):

        self.staff_user = User.objects.create(username='user1', is_staff=True)
        self.staff_user.set_password('test')
        self.user2 = User.objects.create(username='user2')
        self.user2.set_password('test')

        self.staff_user.save()
        self.user2.save()
    def test_series_unicode(self):
        series = Series(title='foo', description='bar')
        series.save()
        self.assertEqual(u'foo', str(series))

    def test_entry_get_html_content(self):
        """ Tests the get_html_content method used in the admin template
        to link to the entry to preview
        """
        entry = Entry(owner=self.user2, title='foo', content='bar')
        entry.save()
        content = entry.get_html_content()

        # We don't care what the HTML looks like, just that it contains a link
        # to the entry
        self.assertTrue(content.find(entry.get_absolute_url()) > 0)
        self.assertTrue(hasattr(entry.get_html_content, 'allow_tags'))

    def test_entry_unicode(self):
        entry = Entry(owner=self.user2, title='foo', content='bar')
        entry.save()
        self.assertEqual(u'foo', str(entry))
