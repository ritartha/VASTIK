"""
Gallery App — Models
"""
from django.db import models


class GalleryImage(models.Model):
    """An image displayed in the VASTIK gallery."""

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(
        default=True,
        help_text="Only visible images are shown on the website"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title
