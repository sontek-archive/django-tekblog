from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

""" The types of markup that are available """
markup_choices = (
    ('rst', 'reStructuredText'),
    ('txl', 'Textile'),
    ('mrk', 'Markdown'),
)

""" Allows us to preview posts before we push them live """
status_choices = (
    (1, 'Draft'),
    (2, 'Public'),
)

class Blog(models.Model):
    """ 
        Blog Model
        Represents an individual blog, allows us to have 
        multiple blogs on a single site.
    """
    owner           = models.ForeignKey(User)
    title           = models.CharField(max_length=100)
    tagline         = models.CharField(max_length=200, blank=True, null=True)
    slug            = models.SlugField(max_length=100)
    posts_per_page  = models.IntegerField(default=20)

    def __unicode__(self):
        return unicode(self.title)

class Series(models.Model):
    """ Series Model
        Link a collection of blogs together so the user
        can easily follow along
    """
    title           = models.CharField(max_length=100)
    description     = models.TextField()

class ActiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveEntryManager, self).get_query_set().filter(status=2, published_on__lte=datetime.now)

class Entry(models.Model):
    """ Entry Model """
    blog            = models.ForeignKey(Blog)
    series          = models.ForeignKey(Series, blank=True, null=True)
    title           = models.CharField(max_length=255)
    creator_ip      = models.IPAddressField(blank=True, null=True)
    status          = models.IntegerField(choices=status_choices, default=2)
    allow_comments  = models.BooleanField(default=True)
    created_on      = models.DateTimeField(default=datetime.now)
    published_on    = models.DateTimeField(default=datetime.now)
    last_updated_on = models.DateTimeField(editable=False, null=True, blank=True)
    slug            = models.SlugField()
    content         = models.TextField()
    markup          = models.CharField(max_length=3, choices=markup_choices, null=True, blank=True)
    active_objects  = ActiveEntryManager()
    
    class Meta:
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return unicode(self.title)

    def save(self):
        self.last_updated = datetime.now()
        super(Entry, self).save()
