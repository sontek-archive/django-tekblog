from haystack.forms import SearchForm
from django.db.models import Q

class EntrySearchForm(SearchForm):
    def search(self):
        sqs = self.searchqueryset
        if self.cleaned_data['q']:
            text = self.cleaned_data['q']
            sqs = sqs.filter(
                        Q(text__icontains=text) |
                        Q(title__icontains=text) |
                        Q(content__icontains=text) |
                        Q(tags__icontains=text))
        return sqs
