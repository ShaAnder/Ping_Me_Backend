from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer to create an Account for the user"""
    
    owner = serializers.ReadOnlyField(source='owner.username')
    
    # Annotate to prevent Spectacular warning
    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'location',
            'content', 'image', 'image_url'
        ]