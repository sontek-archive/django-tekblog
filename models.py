from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from tagging.fields import TagField

""" The types of markup that are available """
markup_choices = (
    ('rst', 'reStructuredText'),
    ('txl', 'Textile'),
    ('mrk', 'Markdown'),
    ('html', 'Html'),
)

""" Allows us to preview posts before we push them live """
status_choices = (
    (1, 'Draft'),
    (2, 'Public'),
)

""" Locales the blog can be translated to  """
entry_locales = (
    ('en', 'English'),
    ('es', 'Espanol'),
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
    def published(self):
        return super(ActiveEntryManager, self).get_query_set().filter(status=2, published_on__lte=datetime.now)

class Entry(models.Model):
    """ Entry Model """
    blog            = models.ForeignKey(Blog)
    series          = models.ForeignKey(Series, blank=True, null=True)
    title           = models.CharField(max_length=255)
    creator_ip      = models.IPAddressField(blank=True, null=True)
    status          = models.IntegerField(choices=status_choices, default=2)
    allow_comments  = models.BooleanField(default=True)
    created_dat     = models.DateTimeField(default=datetime.now)
    pub_date        = models.DateTimeField(default=datetime.now)
    update_date     = models.DateTimeField(editable=False, null=True, blank=True)
    slug            = models.SlugField()
    content         = models.TextField()
    markup          = models.CharField(max_length=4, choices=markup_choices, null=True, blank=True)
    locale          = models.CharField(max_length=5, choices=entry_locales, default="en")
    objects         = ActiveEntryManager()
    tags            = TagField()

    def get_absolute_url(self):
        return ('entry_detail', (), {
            'locale': self.locale,
            'slug': self.slug,
        })

    def __unicode__(self):
        return unicode(self.title)

    def save(self):
        self.last_updated = datetime.now()
        super(Entry, self).save()

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ('-pub_date',)
