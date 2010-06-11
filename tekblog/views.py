from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tekblog.models import Entry
from django.core.paginator import Paginator

def index(request, page=1, template='tekblog/index.html'):
    paginator = Paginator(Entry.objects.active(), 5)
    pager = paginator.page(page)
    return render_to_response(template, {'pager': pager},
            context_instance=RequestContext(request))

def detail(request, slug, template='tekblog/detail.html'):
    entry = get_object_or_404(Entry, slug=slug)

    return render_to_response(template, {'entry': entry},
            context_instance=RequestContext(request))
