"""
Store App — Serializers
"""
from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images."""

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products with nested images."""

    images = ProductImageSerializer(many=True, read_only=True)
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'serial_number', 'name', 'category', 'category_display',
            'description', 'price', 'marketplace_url', 'inworld_slurl',
            'is_featured', 'created_at', 'images',
        ]
