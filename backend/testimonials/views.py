"""
Testimonials App — Views
"""
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Testimonial
from .serializers import TestimonialSerializer


class TestimonialListView(ListAPIView):
    """
    GET /api/v1/testimonials/
    Returns all visible testimonials.
    """
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.filter(is_visible=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
        })
