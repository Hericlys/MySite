"""
Attachment model
"""
from django_summernote.models import AbstractAttachment
from utils.images import resize_image


class FilesAttachment(AbstractAttachment):
    """class"""
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        current_file_name = str(self.file.name)
        super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900)