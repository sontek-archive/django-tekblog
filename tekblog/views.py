import re
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tekblog.models import Entry
from django.core.paginator import Paginator, InvalidPage
from haystack.views import SearchView
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from tekblog.forms import EntrySearchForm
from django.http import Http404
from tagging.models import TaggedItem

def index(request, page=1, topic=None, template='tekblog/index.html'):
    active_entries = Entry.objects.active(is_staff=request.user.is_staff)

    if topic:
        active_entries = TaggedItem.objects.get_by_model(active_entries, topic)

    paginator = Paginator(active_entries, 5)
    pager = paginator.page(page)
    return render_to_response(template, {'pager': pager},
            context_instance=RequestContext(request))
    
def detail(request, slug, template='tekblog/detail.html'):
    entry = get_object_or_404(Entry, slug=slug)
    if (entry.draft and request.user.is_staff) or not entry.draft:
        return render_to_response(template, {'entry': entry},
                context_instance=RequestContext(request))
    else:
        raise Http404("No such entry")

def search(request, template='tekblog/search.html'):
    entries = Entry.objects.all()

    query = ''
    searchqueryset = SearchQuerySet().models(Entry)
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        form = EntrySearchForm(request.GET, searchqueryset=searchqueryset, load_all=True)
        if form.is_valid():
            query = request.GET.get('q') 
            results = form.search(is_staff=request.user.is_staff)
            paginator = Paginator(results, 1000)
    else:
        form = EntrySearchForm(searchqueryset=searchqueryset, load_all=True)
        paginator = Paginator(entries, 1000)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")
    
    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'results': results,
    }

    return render_to_response(template, context, context_instance=RequestContext(request))
