from django.contrib import admin
from .models import *

from .models import MessageSession, Message, MessageFile

admin.site.register(MessageSession)
admin.site.register(Message)
admin.site.register(MessageFile)
