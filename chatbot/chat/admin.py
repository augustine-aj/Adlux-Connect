from django.contrib import admin
from .models import ChatSession, Interaction

admin.site.register(ChatSession)
admin.site.register(Interaction)