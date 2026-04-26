"""
VASTIK URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def index(request):
    """Render the main single-page application."""
    return render(request, 'index.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('store.urls')),
    path('api/v1/gallery/', include('gallery.urls')),
    path('api/v1/contact/', include('contact.urls')),
    path('', index, name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
