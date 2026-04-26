"""
Gallery App — Serializers
"""
from rest_framework import serializers
from .models import GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for gallery images."""
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'image', 'description', 'category',
                  'category_display', 'uploaded_at']
