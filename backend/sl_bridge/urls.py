"""
SL Bridge App — URL Configuration
"""
from django.urls import path
from .views import RegisterSLURLView

urlpatterns = [
    path('register-url/', RegisterSLURLView.as_view(), name='sl-bridge-register-url'),
]
