from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ping_me_api.utils import validate_image_file  # Adjust path if needed

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer to create an Account for the user"""

    owner = serializers.ReadOnlyField(source="owner.username")

    image = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField()

    def validate_image(self, value):
        return validate_image_file(value)

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    class Meta:
        model = Account
        fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "username",
            "location",
            "content",
            "image",
            "image_url",
        ]
