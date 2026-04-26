"""
Gallery App — Models
"""
from django.db import models


class GalleryImage(models.Model):
    """An image displayed in the VASTIK gallery."""

    CATEGORY_CHOICES = [
        ('Build', 'In-World Builds'),
        ('Product', 'Product Showcase'),
        ('Event', 'Events & Meetups'),
        ('Art', 'Concept Art'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(
        blank=True,
        help_text="Optional description shown in lightbox view"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Build',
        help_text="Category for filtering"
    )
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
