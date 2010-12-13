from django.contrib import admin
from tekblog.models import Series, Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_html_content', 'tags', 'published_on',
            'draft')

    fieldsets = (
        ('General', {
            'fields': ['title', 'owner', 'tags', 'published_on', 'draft',
                'sites', 'featured', 'allow_comments'],
            'classes': ('colMS',),
        }),
        ('Content', {
            'fields': ['content', 'markup', ],
            'classes': ('colM',),
        }), 
        ('Optional', {
            'fields': ['keywords', 'description', 'related_content'],
            'classes': ('colM', 'collapsible', 'collapse'),
        }),
    )
    change_form_template = 'admin/tekblog/entry/change_form.html'

admin.site.register(Series)
admin.site.register(Entry, EntryAdmin)
