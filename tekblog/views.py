from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tekblog.models import Entry

def index(request):
    active = Entry.objects.active()
    return render_to_response('tekblog/index.html', {'entries': active},
            context_instance=RequestContext(request))

def detail(request, slug):
    entry = get_object_or_404(Entry, slug=slug)

    return render_to_response('tekblog/detail.html', {'entry': entry},
            context_instance=RequestContext(request))
    
