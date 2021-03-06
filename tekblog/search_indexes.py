import datetime
from haystack.indexes import (RealTimeSearchIndex, CharField, BooleanField)
from haystack import site
from tekblog.models import Entry
from django.db.models.signals import post_save


class EntryIndex(RealTimeSearchIndex):
    text = CharField(document=True)
    title = CharField(model_attr='title')
    content = CharField(model_attr='content')
    tags = CharField(model_attr='tags')
    draft = BooleanField(model_attr='draft')

site.register(Entry, EntryIndex)
