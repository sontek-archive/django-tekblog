from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from datetime import datetime
from tagging.fields import TagField
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.comments.moderation import CommentModerator, moderator
from django_extensions.db.fields import AutoSlugField

from formatters import parse_content_with_code

class Series(models.Model):
    """ Series Model
        Link a collection of blogs together so the user
        can easily follow along
    """
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name_plural = 'Series'


class ActiveEntryManager(models.Manager):

    def active(self, is_staff=False):
        if is_staff:
            return self.filter(sites__id__exact=settings.SITE_ID)
        else:
            return self.filter(draft=False, published_on__lte=datetime.now,
                    sites__id__exact=settings.SITE_ID)


MARKUP_CHOICE_DEFAULTS = (
    # class, # display text
    (None, 'None'),
    ('linebreaks', 'Linebreaks'),
    ('textile_formatter', 'Textile'),
    ('markdown_formatter', 'Markdown'),
)

MARKUP_CHOICES = getattr(settings, 'TEKBLOG_MARKUP_CHOICES',
        MARKUP_CHOICE_DEFAULTS)

class Entry(models.Model):
    """ Base class for blog entries """
    owner = models.ForeignKey(User)
    series = models.ForeignKey(Series, blank=True, null=True)
    featured = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    creator_ip = models.IPAddressField(blank=True, null=True)
    draft = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='title')
    content = models.TextField()
    html_content = models.TextField(editable=False, blank=True)
    markup = models.CharField(max_length=255,
            choices=MARKUP_CHOICES)
    objects = ActiveEntryManager()
    tags = TagField()
    sites = models.ManyToManyField(Site)

    # Dates
    created_on = models.DateTimeField(default=datetime.now)
    published_on = models.DateTimeField(default=datetime.now)
    modified_on = models.DateTimeField(blank=True, null=True)

    # SEO
    keywords = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # Used to display "You might be interested in..."
    related_content = models.ManyToManyField('self', null=True, blank=True)

    def get_html_content(self):
        """We can only assign allow_tags to methods"""
        return '<a href="%s" target="_blank">%s</a><br />%s' % (
                self.get_absolute_url(),
                self.title, self.html_content)

    get_html_content.allow_tags = True

    def save(self):
        self.html_content = parse_content_with_code(self.markup, self.content)
        super(Entry, self).save()

    @permalink
    def get_absolute_url(self):
        return ('tekblog_detail', (),
                {
                    'slug': self.slug
                }
        )

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ('-published_on',)


class EntryModerator(CommentModerator):
    email_notification = True
    enable_field = 'allow_comments'

moderator.register(Entry, EntryModerator)
