from rest_framework import serializers

from .models import Server, ServerCategory


class ServerSerializer(serializers.ModelSerializer):

  class Meta:
    model = Server
    fields = "__all__"