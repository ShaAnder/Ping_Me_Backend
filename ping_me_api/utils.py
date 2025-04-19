from PIL import Image
from rest_framework.exceptions import ValidationError

ALLOWED_IMAGE_FORMATS = ['jpeg', 'jpg', 'png', 'webp']
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
            raise ValidationError(f"Unsupported image format '{format}'. Allowed formats: {', '.join(ALLOWED_IMAGE_FORMATS)}.")
    except Exception:
        raise ValidationError("Invalid image file.")

    return image_file
