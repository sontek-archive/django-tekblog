from tekblog.forms import EntrySearchForm
def search_form(request):
    if request.GET:
        form = EntrySearchForm(request.GET)
    else:
        form = EntrySearchForm()

    return {'entry_search_form': form }
