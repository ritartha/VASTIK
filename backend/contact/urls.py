"""
Contact App — URL Configuration
"""
from django.urls import path
from .views import SendOTPView, VerifyOTPView, SubmitContactView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='contact-send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='contact-verify-otp'),
    path('submit/', SubmitContactView.as_view(), name='contact-submit'),
]
