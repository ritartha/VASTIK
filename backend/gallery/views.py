"""
Gallery App — Views
"""
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import GalleryImage
from .serializers import GalleryImageSerializer


class GalleryListView(ListAPIView):
    """
    GET /api/v1/gallery/
    GET /api/v1/gallery/?category=Build
    Returns all visible gallery images, optionally filtered by category.
    """
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_visible=True)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
        })
