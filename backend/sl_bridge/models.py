"""
SL Bridge App — Models
Stores the dynamic Second Life object URL that resets on region restart.
"""
from django.db import models


class SLObjectURL(models.Model):
    """
    Stores the current LSL object URL.
    Only one active URL should exist at a time — the latest registration
    from the in-world object after each region restart.
    """

    object_url = models.URLField(
        max_length=500,
        help_text="The dynamic URL provided by llRequestURL() in Second Life"
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this URL is currently reachable"
    )

    class Meta:
        ordering = ['-registered_at']
        verbose_name = 'SL Object URL'
        verbose_name_plural = 'SL Object URLs'

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"[{status}] {self.object_url[:80]}... ({self.registered_at})"

    @classmethod
    def get_active_url(cls):
        """Return the most recently registered active URL, or None."""
        return cls.objects.filter(is_active=True).first()
