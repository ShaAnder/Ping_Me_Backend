from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from .models import Channel, Server, ServerCategory


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"
        read_only_fields = ["owner"]


class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True, read_only=True)
    owner_id = serializers.ReadOnlyField(source="owner.id")
    owner = serializers.ReadOnlyField(source="owner.owner.username")
    category_name = serializers.CharField(source="category.name", read_only=True)

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_server_image_urls(self, obj):
        # Check for server_icon and banner_image
        image_urls = {}
        if obj.server_icon:
            image_urls["server_icon_url"] = obj.server_icon.url
        if obj.banner_image:
            image_urls["banner_image_url"] = obj.banner_image.url
        return image_urls

    server_image_urls = serializers.SerializerMethodField()
    server_icon = serializers.ImageField(write_only=True, required=False)
    banner_image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Server
        fields="__all__"

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and not validated_data.get("owner"):
            validated_data["owner"] = request.user

        with transaction.atomic():  # Enforce atomicity
            server = Server.objects.create(**validated_data)

            Channel.objects.create(
                name="general",
                type=Channel.text,
                server=server,
                owner=request.user,
                description="General text chat",
            )
            Channel.objects.create(
                name="vc gener", type=Channel.voice, server=server, owner=request.user
            )

        return server


class ServerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerCategory
        fields = "__all__"

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_category_icon_url(self, obj):
        # Safely try to get the image URL
        image = getattr(obj, "category_image", None)
        if image and hasattr(image, "url"):
            return image.url
        return None

    category_icon_url = serializers.SerializerMethodField()
    category_icon = serializers.ImageField(write_only=True, required=False)
    permission_classes = [AllowAny]