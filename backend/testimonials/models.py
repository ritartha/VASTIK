"""
Testimonials App — Models
Customer testimonials for the VASTIK store.
"""
from django.db import models


class Testimonial(models.Model):
    """A customer testimonial/review for the VASTIK store."""

    sl_name = models.CharField(
        max_length=100,
        verbose_name="SL Name",
        help_text="The customer's Second Life username"
    )
    quote = models.TextField(
        help_text="The testimonial text"
    )
    rating = models.PositiveIntegerField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
        default=5,
        help_text="Star rating from 1 to 5"
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Only visible testimonials are shown on the website"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.sl_name} — {self.rating}★"
