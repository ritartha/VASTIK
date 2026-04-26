"""
Testimonials App — Serializers
"""
from rest_framework import serializers
from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    """Serializer for testimonials."""

    class Meta:
        model = Testimonial
        fields = ['id', 'sl_name', 'quote', 'rating', 'created_at']
