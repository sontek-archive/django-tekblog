from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from datetime import datetime
from tagging.fields import TagField
from django.contrib.sites.models import Site
from django.conf import settings
from utils import Formatter

formatter = Formatter()

class Series(models.Model):
    """ Series Model
        Link a collection of blogs together so the user
        can easily follow along
    """
    title           = models.CharField(max_length=100)
    description     = models.TextField()

class ActiveEntryManager(models.Manager):
    def active(self):
        return self.filter(draft=False, published_on__lte=datetime.now, 
                sites__id__exact=settings.SITE_ID)

class Entry(models.Model):
    """ Base class for blog entries """
    owner           = models.ForeignKey(User)
    series          = models.ForeignKey(Series, blank=True, null=True)
    featured        = models.BooleanField(default=False)
    title           = models.CharField(max_length=255)
    creator_ip      = models.IPAddressField(blank=True, null=True)
    draft           = models.BooleanField(default=True)
    allow_comments  = models.BooleanField(default=True)
    slug            = models.SlugField()
    content         = models.TextField()
    html_content    = models.TextField(editable=False, blank=True)
    markup          = models.CharField(max_length=4, choices=formatter.MARKUP_CHOICES)
    objects         = ActiveEntryManager()
    tags            = TagField()
    sites           = models.ManyToManyField(Site)

    # Dates
    created_on      = models.DateTimeField(default=datetime.now)
    published_on    = models.DateTimeField(default=datetime.now)
    modified_on     = models.DateTimeField(blank=True, null=True)

    # SEO
    keywords        = models.CharField(max_length=200, null=True, blank=True)
    description     = models.TextField(null=True, blank=True)

    # Used to display "You might be interested in..."
    related_content = models.ManyToManyField('self', null=True, blank=True)

    def save(self):
        self.html_content = formatter.format(self.markup, self.content) 
        super(Entry, self).save()

    @permalink
    def get_absolute_url(self):
        return ('tekblog_detail', (), 
                { 'slug': self.slug }
        )

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ('-published_on',)
