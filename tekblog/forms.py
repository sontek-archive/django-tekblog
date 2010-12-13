from django.db.models import Q
from django import forms
from tekblog.models import Entry
from haystack.forms import SearchForm


class EntrySearchForm(SearchForm):

    def search(self, is_staff=False):
        sqs = self.searchqueryset
        if self.cleaned_data['q']:
            text = self.cleaned_data['q']
            sqs = sqs.filter(
                        Q(text__icontains=text) |
                        Q(title__icontains=text) |
                        Q(content__icontains=text) |
                        Q(tags__icontains=text))

            if not is_staff:
                sqs = sqs.filter(draft=False)

        return sqs.highlight()
