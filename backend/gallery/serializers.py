"""
Gallery App — Serializers
"""
from rest_framework import serializers
from .models import GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for gallery images."""

    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'image', 'uploaded_at']
