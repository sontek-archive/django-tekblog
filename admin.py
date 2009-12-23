from django.contrib import admin
from tekblog.models import Entry, Blog

class EntryAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ('title',)}

class BlogAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ('title',)}

admin.site.register(Entry, EntryAdmin)
admin.site.register(Blog, BlogAdmin)
