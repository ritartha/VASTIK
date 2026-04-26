"""
Store App — Views
Class-based API views for products.
"""
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductListView(ListAPIView):
    """
    GET /api/v1/products/
    GET /api/v1/products/?category=Mesh
    Returns a list of all products, optionally filtered by category.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images').all()
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


class ProductDetailView(RetrieveAPIView):
    """
    GET /api/v1/products/<id>/
    Returns a single product with all images.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('images').all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
        })
