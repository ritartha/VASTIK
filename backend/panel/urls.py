"""
Panel App — URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.panel_login, name='panel-login'),
    path('logout/', views.panel_logout, name='panel-logout'),
    path('', views.panel_dashboard, name='panel-dashboard'),
    path('products/', views.panel_products, name='panel-products'),
    path('products/add/', views.panel_product_add, name='panel-product-add'),
    path('products/<int:pk>/edit/', views.panel_product_edit, name='panel-product-edit'),
    path('products/<int:pk>/delete/', views.panel_product_delete, name='panel-product-delete'),
]
