from django.contrib import admin

from .models import Channel, Server, ServerCategory

admin.site.register(Channel)
admin.site.register(Server)
admin.site.register(ServerCategory)