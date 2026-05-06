"""
Store App — Serializers
"""
from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images."""

    image_src = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'image_src', 'order']

    def get_image_src(self, obj):
        """Return image_url if set, otherwise fall back to uploaded image."""
        if obj.image_url:
            return obj.image_url
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ''


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
