from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tekblog.models import Entry
from django.core.paginator import Paginator

def index(request, page=1):
    paginator = Paginator(Entry.objects.active(), 5)
    pager = paginator.page(page)
    return render_to_response('tekblog/index.html', {'pager': pager},
            context_instance=RequestContext(request))

def detail(request, slug):
    entry = get_object_or_404(Entry, slug=slug)

    return render_to_response('tekblog/detail.html', {'entry': entry},
            context_instance=RequestContext(request))
    
