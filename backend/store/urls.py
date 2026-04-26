"""
Store App — URL Configuration
"""
from django.urls import path
from .views import ProductListView, ProductDetailView, FeaturedProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('featured/', FeaturedProductListView.as_view(), name='product-featured'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
