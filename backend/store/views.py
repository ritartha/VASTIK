"""
Store App — Views
Class-based API views for products.
"""
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductListView(ListAPIView):
    """
    GET /api/v1/products/
    GET /api/v1/products/?category=Mesh
    GET /api/v1/products/?search=temple
    GET /api/v1/products/?ordering=-price
    Returns a list of all products with search, filter, and sort support.
    """
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'serial_number', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['-created_at']

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


class FeaturedProductListView(ListAPIView):
    """
    GET /api/v1/products/featured/
    Returns only featured products for the home page carousel.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('images').filter(is_featured=True)
    pagination_class = None  # No pagination for featured carousel

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
        })
