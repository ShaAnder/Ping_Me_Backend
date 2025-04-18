from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Server, ServerCategory


class ServerSerializer(serializers.ModelSerializer):

  owner = serializers.ReadOnlyField(source='owner.username')

  # Annotate to prevent Spectacular warning
  @extend_schema_field(serializers.CharField(allow_null=True))
  def get_server_image_url(self, obj):
      return obj.server_image.url if obj.server_image else None

  server_image_url = serializers.SerializerMethodField()
  server_image = serializers.ImageField(write_only=True, required=False)

  class Meta:
    model = Server
    fields = "__all__"