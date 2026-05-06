"""
Store App — Models
Product and ProductImage models for the VASTIK marketplace.
"""
from django.db import models


class Product(models.Model):
    """A product available in the VASTIK Second Life store."""

    CATEGORY_CHOICES = [
        ('Mesh', 'Mesh'),
        ('Script', 'Script'),
        ('Texture', 'Texture'),
    ]

    serial_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique serial number, e.g. VTK-001"
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        help_text="Price in L$ (Linden Dollars)"
    )
    marketplace_url = models.URLField(
        blank=True,
        help_text="Second Life Marketplace URL"
    )
    inworld_slurl = models.URLField(
        blank=True,
        help_text="In-world SLurl (secondlife:// protocol)"
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.serial_number} — {self.name}"


class ProductImage(models.Model):
    """Images associated with a product, ordered for slideshow display."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text="Upload an image file (optional if image_url is set)"
    )
    image_url = models.URLField(
        blank=True,
        default='',
        help_text="External image URL (used instead of uploaded file)"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order in slideshow (lower = first)"
    )

    class Meta:
        ordering = ['order']

    @property
    def src(self):
        """Return the best available image source URL."""
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''

    def __str__(self):
        return f"Image {self.order} for {self.product.name}"
