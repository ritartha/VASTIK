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
    Returns all visible gallery images.
    """
    serializer_class = GalleryImageSerializer
    queryset = GalleryImage.objects.filter(is_visible=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
        })
