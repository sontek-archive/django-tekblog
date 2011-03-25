from unittest import TestCase
from mock import patch, Mock
from django.http import Http404

from tekblog.views import index, detail, search
from django.core.paginator import InvalidPage

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


    @patch('tekblog.views.render_to_response')
    @patch('tekblog.views.RequestContext')
    def test_detail_draft_entry_staff(self, renderer, request_context):
        """
        Tests that a staff viewing a draft entry can see it.
        """
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.return_value = self.entry
            self.entry.draft = True
            self.request.user.is_staff = True

            detail(self.request, self.slug, template=self.details_template)
            self.assertTrue(renderer.called)


    @patch('tekblog.views.render_to_response')
    @patch('tekblog.views.RequestContext')
    def test_detail_not_draft_staff(self, renderer, request_context):
        """
        Tests that a anyone viewing an entry can see it.
        """
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.return_value = self.entry
            self.entry.draft = False
            self.request.user.is_staff = False

            detail(self.request, self.slug, template=self.details_template)
            self.assertTrue(renderer.called)


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
        with patch('tekblog.views.Entry.objects.active') as active_call:
            active_call.return_value = self.results
            index(self.request)

            self.assertTrue(active_call.called)
            self.assertFalse(get_by_model_call.called)

    @patch('tekblog.views.Paginator')
    @patch('tekblog.views.TaggedItem.objects.get_by_model')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_default_index_topic(self, r2r, rc, get_by_model_call, paginator):
        with patch('tekblog.views.Entry.objects.active') as active_call:
            active_call.return_value = self.results
            index(self.request, topic='Hello')

            get_by_model_call.assert_called_with(self.results, '"Hello"')

            self.assertTrue(active_call.called)
            self.assertTrue(get_by_model_call.called)

    @patch('tekblog.views.Entry.objects.active')
    @patch('tekblog.views.TaggedItem.objects.get_by_model')
    @patch('tekblog.views.RequestContext')
    @patch('tekblog.views.render_to_response')
    def test_default_index_invalid_page(self, r2r, rc, get_by_model_call, active_call):
        with patch('tekblog.views.Paginator') as paginator:
            instance = paginator.return_value
            instance.page.side_effect = InvalidPage()

            self.assertRaises(Http404, index, self.request)
            self.assertTrue(active_call.called)
            self.assertFalse(get_by_model_call.called)
