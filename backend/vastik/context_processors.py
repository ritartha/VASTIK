"""
VASTIK — Context Processors
Injects social links and other global data into all templates.
"""
from django.conf import settings


def social_links(request):
    """Add social media links to template context."""
    return {
        'social_links': settings.SOCIAL_LINKS,
    }
