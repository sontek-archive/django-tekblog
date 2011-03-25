from unittest import TestCase
from mock import patch, Mock
from django.http import Http404

from tekblog.views import index, detail, search

class MockException(Exception):
    pass

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
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.side_effect = MockException()
            self.assertRaises(MockException, detail, self.request, self.slug)

    def test_detail_draft_entry_not_staff(self):
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.side_effect = self.entry
            self.entry.draft.return_value = True
            self.request.user.is_staff.return_value = False
            self.assertRaises(Http404, detail, self.request, self.slug)

    @patch('tekblog.views.render_to_response')
    @patch('tekblog.views.RequestContext')
    def test_detail_draft_entry_staff(self, renderer, request_context):
        with patch('tekblog.views.get_object_or_404') as getter:
            getter.side_effect = self.entry
            self.entry.draft.return_value = True
            self.request.user.is_staff.return_value = True

            detail(self.request, self.slug, template=self.details_template)
            renderer.assert_called_with(self.details_template,
                {'entry': self.entry})
