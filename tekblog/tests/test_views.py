from django.test import TestCase
from mock import patch, Mock

from django.http import Http404
from django.core.paginator import InvalidPage
from django.test.client import Client
from django.contrib.auth.models import User

from tekblog.tests.test_helpers import get_context
from tekblog.views import index, detail, search
from tekblog.models import Entry


class DetailViewTests(TestCase):
    """
    Tests the basic functionality of each view.
    """
    def setUp(self):
        self.request = Mock()
        self.entry = Mock()
        self.slug = 'Hello world'
        self.details_template = Mock()


    def test_detail_invalid_entry(self):
        """
        Tests that an invalid entry raises an exception on object_or_404.
        """
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.side_effect = Http404()
            self.assertRaises(Http404, detail, self.request, self.slug)


    def test_detail_draft_entry_not_staff(self):
        """
        Tests that the draft entry raises an Http404 for normal users.
        """
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.return_value = self.entry
            self.entry.draft = True
            self.request.user.is_staff = False

            self.assertRaises(Http404, detail, self.request, self.slug)


    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_detail_draft_entry_staff(self, r2r, request_context):
        """
        Tests that a staff viewing a draft entry can see it.
        """
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.return_value = self.entry
            self.entry.draft = True
            self.request.user.is_staff = True

            detail(self.request, self.slug, template=self.details_template)
            self.assertTrue(r2r.called)
            self.assertTrue(get_context(r2r).has_key('entry'))


    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_detail_not_draft_staff(self, r2r, request_context):
        """
        Tests that a anyone viewing an entry can see it.
        """
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.return_value = self.entry
            self.entry.draft = False
            self.request.user.is_staff = False

            detail(self.request, self.slug, template=self.details_template)
            self.assertTrue(r2r.called)
            self.assertTrue(get_context(r2r).has_key('entry'))


class IndexViewTests(TestCase):
    """
    Tests the basic conditions of the index view.
    """
    def setUp(self):
        self.request = Mock()
        self.results = Mock()


    @patch('tekblog.views.Paginator')
    @patch('tekblog.views.TaggedItem.objects.get_by_model')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_default_index(self, r2r, rc, get_by_model_call, paginator):
        """
        Tests that the normal flow of getting active items and rendering 
        a response is called without a call to the get topics.
        """
        with patch('tekblog.views.Entry.objects.active') as active_call:
            active_call.return_value = self.results
            index(self.request)

            self.assertTrue(active_call.called)
            self.assertFalse(get_by_model_call.called)
            self.assertTrue(r2r.called)
            self.assertTrue(get_context(r2r).has_key('pager'))


    @patch('tekblog.views.Paginator')
    @patch('tekblog.views.TaggedItem.objects.get_by_model')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_default_index_topic(self, r2r, rc, get_by_model_call, paginator):
        """
        Tests that the normal flow of getting active items and rendering
        a response is called in addition to using the topic.
        """
        with patch('tekblog.views.Entry.objects.active') as active_call:
            active_call.return_value = self.results
            index(self.request, topic='Hello')

            get_by_model_call.assert_called_with(self.results, '"Hello"')

            self.assertTrue(active_call.called)
            self.assertTrue(get_by_model_call.called)
            self.assertTrue(r2r.called)
            self.assertTrue(get_context(r2r).has_key('pager'))


    @patch('tekblog.views.Entry.objects.active')
    @patch('tekblog.views.TaggedItem.objects.get_by_model')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_default_index_invalid_page(self, r2r, rc, get_by_model_call, active_call):
        """
        Tests that the normal flow of getting active items and rendering
        is not done as a result of an invalid page thus returning a 404.
        """
        with patch('tekblog.views.Paginator') as paginator:
            instance = paginator.return_value
            instance.page.side_effect = InvalidPage()

            self.assertRaises(Http404, index, self.request)
            self.assertTrue(active_call.called)
            self.assertFalse(get_by_model_call.called)
            self.assertFalse(r2r.called)


class SearchViewTests(TestCase):
    """
    Tests basic view functionality within the search.
    """
    def setUp(self):
        self.request = Mock()
        self.request.GET = {}

        self.staff_user = User.objects.create(username='user1', is_staff=True)
        self.staff_user.set_password('test')
        self.user2 = User.objects.create(username='user2')
        self.user2.set_password('test')

        self.staff_user.save()
        self.user2.save()

    @patch('tekblog.views.Paginator')
    @patch('tekblog.views.EntrySearchForm')
    @patch('tekblog.views.EmptySearchQuerySet')
    @patch('tekblog.views.SearchQuerySet')
    @patch('tekblog.views.Entry.objects.all')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_search_no_query_default(self, r2r, rc, all_call, sqs, empty_sqs, frm, pager):
        search(self.request)

        self.assertTrue(frm.called)
        self.assertFalse(frm.return_value.is_valid.called)

        # Ensure that render_to_response returns all the right context variables
        self.assertTrue(r2r.called)
        context = get_context(r2r)
        self.assertEquals(context['form'], frm.return_value)
        self.assertEquals(context['page'], pager.return_value.page.return_value)
        self.assertEquals(context['paginator'], pager.return_value)
        self.assertEquals(context['query'], '')

        # The default results should be an empty query set
        self.assertEquals(context['results'], empty_sqs.return_value)

    @patch('tekblog.views.Paginator')
    @patch('tekblog.views.EntrySearchForm')
    @patch('tekblog.views.EmptySearchQuerySet')
    @patch('tekblog.views.SearchQuerySet')
    @patch('tekblog.views.Entry.objects.all')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_search_query_no_results(self, r2r, rc, all_call, sqs, empty_sqs, frm, pager):
        self.request.GET = {'q': 'tester'}
        search(self.request)

        self.assertTrue(frm.called)
        self.assertTrue(frm.return_value.is_valid.called)
        pager.assert_called_with(frm.return_value.search.return_value, 1000)

        # Ensure that render_to_response returns all the right context variables
        self.assertTrue(r2r.called)
        context = get_context(r2r)
        self.assertEquals(context['form'], frm.return_value)
        self.assertEquals(context['page'], pager.return_value.page.return_value)
        self.assertEquals(context['paginator'], pager.return_value)
        self.assertEquals(context['query'], 'tester')

        # The results should be from the values returned from search
        self.assertEquals(context['results'], frm.return_value.search.return_value)


    @patch('tekblog.views.EntrySearchForm')
    @patch('tekblog.views.EmptySearchQuerySet')
    @patch('tekblog.views.SearchQuerySet')
    @patch('tekblog.views.Entry.objects.all')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_search_query_invalid_page(self, r2r, rc, all_call, sqs, empty_sqs, frm):
        with patch('tekblog.views.Paginator') as paginator:
            instance = paginator.return_value
            instance.page.side_effect = InvalidPage()

            self.request.GET = {'q': 'tester'}
            self.assertRaises(Http404, search, self.request)

            self.assertTrue(frm.called)
            self.assertTrue(frm.return_value.is_valid.called)
            paginator.assert_called_with(frm.return_value.search.return_value, 1000)

            # Ensure that render_to_response was not called
            self.assertFalse(r2r.called)

    def test_search_only_returns_active(self):
        """
        This verifies that only active entries return in the results, unless
        the user is_staff=True
        """

        self.client = Client()

        # We are using db instead of mocking so that the haystack indexes
        # are created
        entry1 = Entry(owner=self.staff_user, title='Python and Django',
                draft=True, tags='python, django', markup=None)
        entry2 = Entry(owner=self.user2, title='Django', draft=False,
                tags='python, django', markup=None)

        entry1.save()
        entry2.save()

        self.client.login(username=self.user2.username, password='test')
        response = self.client.post('/search/?q=python')
        self.assertTrue(len(response.context['results']), 1)
