"""
Module responsible for image manipulation
"""
from pathlib import Path
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from PIL import Image


def resize_image(
    image_django: InMemoryUploadedFile,
    new_width: int = 800,
    optimize: bool = True,
    quality: int = 60
) -> InMemoryUploadedFile:
    """
    Resize image by changing its quality to make files lighter

    Parameters:
    image_django = InMemoryUploadedFile | Image to be resize
    new_width = int | Width of new image
    optimize = bool | Image optimization
    quality = int | image quality (max 100)

    Return: InMemoryUploadedfile
    """
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()
    image_pillow = Image.open(image_path)
    original_width, original_heigth = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return image_pillow

    new_height = round(new_width * original_heigth / original_width)

    new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
    new_image.save(
        image_path,
        optimize=optimize,
        quality=quality,
    )

    return new_image