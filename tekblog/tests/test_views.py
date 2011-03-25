from unittest import TestCase
from mock import patch, Mock
from django.http import Http404

from tekblog.views import index, detail, search

class DefaultViewTest(TestCase):
    """
    Tests the basic functionality of each view.
    """
    def setUp(self):
        self.request = Mock()
        self.entry = Mock()
        self.slug = 'Hello world'
        self.details_template = Mock()

    def test_detail_invalid_entry(self):
        with patch('django.shortcuts.get_object_or_404') as getter:
            getter.side_effect = Http404()
            self.assertRaises(Http404, detail, self.request, self.slug)

    def test_detail_draft_entry_not_staff(self):
        with patch('django.shortcuts.get_object_or_404') as getter:
            getter.side_effect = self.entry
            self.entry.is_draft = True
            self.request.user.is_staff = False
            self.assertRaises(Http404, detail, self.request, self.slug)

    @patch('django.shortcuts.render_to_response')
    @patch('django.template.RequestContext')
    def test_detail_draft_entry_staff(self, renderer, request_context):
        with patch('django.shortcuts.get_object_or_404') as getter:
            getter.side_effect = self.entry
            self.entry.is_draft = True
            self.request.user.is_staff = True

            renderer.assert_called_with(self.details_template,
                {'entry': self.entry},
                request_context)
