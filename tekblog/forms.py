from haystack.forms import SearchForm
from django.db.models import Q

class EntrySearchForm(SearchForm):
    def search(self, is_staff=False):
        sqs = self.searchqueryset#super(EntrySearchForm, self).search()
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
