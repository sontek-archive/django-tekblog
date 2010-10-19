from haystack.forms import SearchForm
from django.db.models import Q

class EntrySearchForm(SearchForm):
    def search(self):
        sqs = self.searchqueryset
        if self.cleaned_data['q']:
            text = self.cleaned_data['q']
            sqs = sqs.filter(
                        Q(title__contains=text) |
                        Q(content__contains=text) |
                        Q(tags__contains=text))
        return sqs
