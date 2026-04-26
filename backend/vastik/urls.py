"""
VASTIK URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def index(request):
    """Render the main home page."""
    return render(request, 'index.html')


def store_page(request):
    """Render the dedicated store/marketplace page."""
    return render(request, 'store.html')


def gallery_page(request):
    """Render the dedicated gallery page."""
    return render(request, 'gallery.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('store.urls')),
    path('api/v1/gallery/', include('gallery.urls')),
    path('api/v1/contact/', include('contact.urls')),
    path('store/', store_page, name='store-page'),
    path('gallery/', gallery_page, name='gallery-page'),
    path('', index, name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
