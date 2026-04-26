"""
Gallery App — Admin Configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Admin for gallery images with thumbnail preview."""
    list_display = ['title', 'image_preview', 'category', 'is_visible', 'uploaded_at']
    list_filter = ['is_visible', 'category', 'uploaded_at']
    list_editable = ['is_visible', 'category']
    search_fields = ['title', 'description']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 4px;" />',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"
