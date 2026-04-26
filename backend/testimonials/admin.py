"""
Testimonials App — Admin Configuration
"""
from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for customer testimonials."""
    list_display = ['sl_name', 'rating_display', 'short_quote', 'is_visible', 'created_at']
    list_filter = ['is_visible', 'rating', 'created_at']
    list_editable = ['is_visible']
    search_fields = ['sl_name', 'quote']

    def rating_display(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_display.short_description = "Rating"

    def short_quote(self, obj):
        return obj.quote[:80] + '...' if len(obj.quote) > 80 else obj.quote
    short_quote.short_description = "Quote"
