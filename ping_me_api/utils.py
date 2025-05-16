from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from PIL import Image
from rest_framework.exceptions import ValidationError

ALLOWED_IMAGE_FORMATS = ["jpeg", "jpg", "png", "webp", "gif"]
MAX_FILE_SIZE_MB = 4
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def validate_image_file(image_file):
    # Validate file size
    if image_file.size > MAX_FILE_SIZE_BYTES:
        raise ValidationError(f"Image size must be under {MAX_FILE_SIZE_MB}MB.")

    # Validate image format using Pillow
    try:
        image = Image.open(image_file)
        format = image.format.lower()
        if format not in ALLOWED_IMAGE_FORMATS:
            raise ValidationError(
                f"Unsupported image format '{format}'. Allowed formats: {', '.join(ALLOWED_IMAGE_FORMATS)}."
            )
    except Exception:
        raise ValidationError("Invalid image file.")

    return image_file

# --- Email verification token functionality ---

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

def generate_token(user):
    """
    Returns a tuple (uidb64, token) for email verification link.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    return uidb64, token

def verify_token(uidb64, token):
    """
    Returns the user if the token is valid, else None.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None

    if token_generator.check_token(user, token):
        return user
    return None
