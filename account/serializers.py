from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
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

class AccountRegistrationSerializer(serializers.ModelSerializer):
    email2 = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['email'] != data['email2']:
            raise serializers.ValidationError("Emails must match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        return data
    
    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data.pop('email2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Inactive until email is verified
        )
        return user
    
class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()