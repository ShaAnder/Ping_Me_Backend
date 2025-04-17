from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer to create a Account for the user

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    # Read only url to display the currently used avatar
    image_url = serializers.ReadOnlyField(source='image.url')
    # Write-only upload for uploading to cloudinary
    image = serializers.ImageField(write_only=True, required=False)  

    class Meta:
        model = Account
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'location',
            'content', 'image', 'image_url'
        ]

    # def get_pfp(self, obj):
    #     image = obj.user_account.image
    #     # If image is a File/Image instance with a .url attribute, return that.
    #     if hasattr(image, 'url'):
    #         return image.url
    #     # Otherwise, assume it's already a URL or a string.
    #     return image