"""
Contact App — Models
Contact messages with OTP verification for Second Life users.
"""
from django.db import models


class ContactMessage(models.Model):
    """A contact message from a Second Life user, verified via OTP."""

    TOPIC_CHOICES = [
        ('Commission Work', 'Commission Work'),
        ('Product Related Issue', 'Product Related Issue'),
        ('Complaints', 'Complaints'),
        ('Suggestions', 'Suggestions'),
        ('Others', 'Others'),
    ]

    sl_name = models.CharField(
        max_length=100,
        verbose_name="SL Name",
        help_text="The user's Second Life username"
    )
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    message = models.TextField()

    # OTP fields
    otp_code = models.CharField(
        max_length=6,
        blank=True,
        help_text="Temporary OTP code for verification"
    )
    otp_verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    # Submission tracking
    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Set after OTP is verified and message is submitted"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Whether an admin has read this message"
    )

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.sl_name} — {self.topic}"
