from django.test import TestCase
from tekblog.models import Series, Entry
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

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

        # clean up the objecs so haystack doesn't have indexes laying around
        entry.delete()


    def test_entry_unicode(self):
        entry = Entry(owner=self.user2, title='foo', content='bar')
        entry.save()
        self.assertEqual(u'foo', str(entry))

        # clean up the objecs so haystack doesn't have indexes laying around
        entry.delete()

    def test_featured_entry_is_first(self):
        """ Featured entries should always be at the beginning of the list """
        entry1 = Entry(owner=self.user2, title='foo1', content='bar',
                draft=False)
        entry1.save()

        entry2 = Entry(owner=self.user2, title='foo2', content='bar',
                featured=True, draft=False)
        entry2.save()

        entry3 = Entry(owner=self.user2, title='foo3', content='bar',
                draft=False)
        entry3.save()

        self.assertEqual(entry2, Entry.objects.all()[0])

        # clean up the objecs so haystack doesn't have indexes laying around
        entry1.delete()
        entry2.delete()
        entry3.delete()


    def test_get_related(self):
        entry1 = Entry(owner=self.user2, title='foo1', content='bar',
                draft=False, tags='python, django')
        entry1.save()
        entry1.sites = Site.objects.all()
        entry1.save()

        entry2 = Entry(owner=self.user2, title='foo2', content='bar',
                featured=True, draft=False, tags='python, django')
        entry2.save()
        entry2.sites = Site.objects.all()
        entry2.save()

        entry3 = Entry(owner=self.user2, title='foo3', content='bar',
                draft=False, tags='python, django')
        entry3.save()
        entry3.sites = Site.objects.all()
        entry3.save()

        self.assertEqual(len(entry3.get_related()), 2)

        entry4 = Entry(owner=self.user2, title='foo3', content='bar',
                draft=False)
        entry4.save()
        entry4.sites = Site.objects.all()
        entry4.related_content.add(entry1)
        entry4.related_content.add(entry2)
        entry4.save()

        self.assertEqual(len(entry4.get_related(max=3)), 2)
        self.assertEqual(len(entry4.get_related(max=1)), 1)

        # clean up the objecs so haystack doesn't have indexes laying around
        entry1.delete()
        entry2.delete()
        entry3.delete()
        entry4.delete()


