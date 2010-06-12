import re

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tekblog.models import Entry
from django.core.paginator import Paginator
from haystack.views import SearchView
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from stopwords import STOP_WORDS

def index(request, page=1, template='tekblog/index.html'):
    paginator = Paginator(Entry.objects.active(), 5)
    pager = paginator.page(page)
    return render_to_response(template, {'pager': pager},
            context_instance=RequestContext(request))

def detail(request, slug, template='tekblog/detail.html'):
    entry = get_object_or_404(Entry, slug=slug)

    return render_to_response(template, {'entry': entry},
            context_instance=RequestContext(request))

def search(request, template='tekblog/search.html'):
    query = ''
    message = ''
    sqs = SearchQuerySet().models(Entry)
    results = EmptySearchQuerySet()

    # Using the search term, filter out any stop words and 
    # leverage the haystack filter on the title, content and tags
    if request.GET:
        stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
        query = '%s' request.GET['q']
        clean_search = stop_word_list.sub('', query)
        clean_search = clean_search.strip()
        if len(clean_data) != 0:
            results = sqs.filter(
                        Q(title__icontains=clean_search) | 
                        Q(content__icontains=clean_search) | 
                        Q(tags__icontains=clean_search))
        else:
            message = 'Search term was too vague. Please revise'

    # Create a paginator for the search results (20 per page)
    paginator = Paginator(results, 20)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'page': page,
        'paginator': paginator,
        'query': query,
        'message': message,
    }

    return render_to_response(template, context, 
            context_instance=RequestContext(request))
