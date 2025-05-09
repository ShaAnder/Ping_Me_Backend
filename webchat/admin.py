from django.contrib import admin

from .models import ConversationModel, Messages

admin.site.register(ConversationModel)
admin.site.register(Messages)
