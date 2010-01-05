from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from datetime import datetime
from tagging.fields import TagField
from django.contrib.sites.models import Site
from django_extensions.db.fields import AutoSlugField, ModificationDateTimeField, CreationDateTimeField

# The types of markup that are available
markup_choices = (
    ('rst', 'reStructuredText'),
    ('txl', 'Textile'),
    ('mrk', 'Markdown'),
    ('html', 'Html'),
)

class Series(models.Model):
    """ Series Model
        Link a collection of blogs together so the user
        can easily follow along
    """
    title           = models.CharField(max_length=100)
    description     = models.TextField()

class ActiveEntryManager(models.Manager):
    def published(self):
        return super(ActiveEntryManager, self).get_query_set().filter(draft=False, published_on__lte=datetime.now)

class Entry(models.Model):
    """ Base class for blog entries """
    owner           = models.ForeignKey(User)
    series          = models.ForeignKey(Series, blank=True, null=True)
    title           = models.CharField(max_length=255)
    creator_ip      = models.IPAddressField(blank=True, null=True)
    draft           = models.BooleanField(default=True)
    allow_comments  = models.BooleanField(default=True)
    slug            = AutoSlugField(populate_from='title')
    content         = models.TextField()
    markup          = models.CharField(max_length=4, choices=markup_choices, null=True, blank=True)
    objects         = models.Manager()
    active_objects  = ActiveEntryManager()
    tags            = TagField()
    sites           = models.ManyToManyField(Site)

    # Dates
    created_on      = CreationDateTimeField(default=datetime.now)
    published_on    = models.DateTimeField(default=datetime.now)
    modified_on     = ModificationDateTimeField()


    # SEO
    keywords        = models.CharField(max_length=200, null=True, blank=True)
    description     = models.TextField(null=True, blank=True)

    # Used to display "You might be interested in..."
    related_content = models.ManyToManyField('self', null=True, blank=True)

    @permalink
    def get_absolute_url(self):
        return ('entry_detail', (), {
            'slug': self.slug,
        })

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ('-published_on',)
