from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Channel, Server, ServerCategory


class ChannelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Channel
    fields = "__all__"

class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.owner.username')

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_server_image_url(self, obj):
        return obj.server_image.url if obj.server_image else None

    server_image_url = serializers.SerializerMethodField()
    server_image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Server
        exclude = ("members",)

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_num_members(self, obj):
      if hasattr(obj, "num_members"):
        return obj.num_members
      return None

    def create(self, validated_data):
        request = self.context.get("request")
        if request and not validated_data.get("owner"):
            validated_data["owner"] = request.user

        server = Server.objects.create(**validated_data)

        # Create default "general" text and voice channels
        Channel.objects.create(
            name="general",
            type=Channel.text,
            server=server,
            owner=request.user,
            description="General text chat"
        )
        Channel.objects.create(
            name="general",
            type=Channel.voice,
            server=server,
            owner=request.user
        )

        return server