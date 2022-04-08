from django.contrib import admin

from .models import Story, StoryFile

admin.site.register(Story)
admin.site.register(StoryFile)
