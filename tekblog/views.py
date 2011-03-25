import re
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tekblog.models import Entry
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from tekblog.forms import EntrySearchForm
from django.http import Http404
from django.conf import settings
from tagging.models import TaggedItem
from haystack.views import SearchView
from haystack.query import EmptySearchQuerySet, SearchQuerySet

ENTRIES_PER_PAGE = getattr(settings, 'TEKBLOG_ENTRIES_PER_PAGE', 5)


def index(request, page=1, topic=None, template='tekblog/index.html'):
    active_entries = Entry.objects.active(is_staff=request.user.is_staff)

    if topic:
        # need to do this so django-tagging will allow muliple words in a tag
        cleaned_topic = '"%s"' % (topic)
        active_entries = TaggedItem.objects.get_by_model(active_entries,
                cleaned_topic)

    paginator = Paginator(active_entries, ENTRIES_PER_PAGE)

    try:
        pager = paginator.page(page)
    except InvalidPage, EmptyPage:
        raise Http404("No such page of results!")

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
        form = EntrySearchForm(request.GET, searchqueryset=searchqueryset,
                load_all=True)
        if form.is_valid():
            query = request.GET.get('q')
            results = form.search(is_staff=request.user.is_staff)
            paginator = Paginator(results, 1000)
    else:
        form = EntrySearchForm(searchqueryset=searchqueryset, load_all=True)
        paginator = Paginator(entries, 1000)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage, EmptyPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'results': results,
    }

    return render_to_response(template, context,
            context_instance=RequestContext(request))
