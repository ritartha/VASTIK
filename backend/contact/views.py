"""
Contact App — Views
OTP send → verify → submit flow using Django's signing module.
"""
import random
import logging
from datetime import timedelta

from django.core import signing
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ContactMessage
from .serializers import SendOTPSerializer, VerifyOTPSerializer, SubmitContactSerializer

logger = logging.getLogger(__name__)

# OTP expiry duration
OTP_EXPIRY_MINUTES = 10
# Signed token expiry (seconds)
TOKEN_EXPIRY_SECONDS = 600  # 10 minutes


class SendOTPView(APIView):
    """
    POST /api/v1/contact/send-otp/
    Accepts {sl_name}, generates a 6-digit OTP, stores it, and logs it.

    In production, this OTP would be delivered via an SL bot or email.
    For now, it's printed to the Django console/log.
    """

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'error': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        sl_name = serializer.validated_data['sl_name']
        otp_code = f"{random.randint(100000, 999999)}"

        # Create or update OTP record for this SL name
        contact, created = ContactMessage.objects.get_or_create(
            sl_name=sl_name,
            otp_verified=False,
            submitted_at__isnull=True,
            defaults={
                'otp_code': otp_code,
                'otp_created_at': timezone.now(),
                'topic': 'Others',
                'message': '',
            }
        )
        if not created:
            contact.otp_code = otp_code
            contact.otp_created_at = timezone.now()
            contact.save(update_fields=['otp_code', 'otp_created_at'])

        # ============================================================
        # IN PRODUCTION: Integrate with SL bot or email service to
        # deliver this OTP to the user's Second Life avatar or email.
        # For now, we print it to the Django console/log.
        # ============================================================
        logger.info(f"[VASTIK OTP] OTP for '{sl_name}': {otp_code}")
        print(f"\n{'='*50}")
        print(f"  VASTIK OTP VERIFICATION")
        print(f"  SL Name: {sl_name}")
        print(f"  OTP Code: {otp_code}")
        print(f"  Expires in: {OTP_EXPIRY_MINUTES} minutes")
        print(f"{'='*50}\n")

        return Response({
            'success': True,
            'data': {
                'message': f'OTP sent to {sl_name}. Check your SL messages.',
            }
        })


class VerifyOTPView(APIView):
    """
    POST /api/v1/contact/verify-otp/
    Accepts {sl_name, otp_code}, validates, and returns a signed token.
    """

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'error': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        sl_name = serializer.validated_data['sl_name']
        otp_code = serializer.validated_data['otp_code']

        try:
            contact = ContactMessage.objects.get(
                sl_name=sl_name,
                otp_verified=False,
                submitted_at__isnull=True,
            )
        except ContactMessage.DoesNotExist:
            return Response({
                'success': False,
                'error': 'No OTP request found for this SL name.',
            }, status=status.HTTP_404_NOT_FOUND)

        # Check OTP expiry
        if contact.otp_created_at:
            expiry_time = contact.otp_created_at + timedelta(minutes=OTP_EXPIRY_MINUTES)
            if timezone.now() > expiry_time:
                return Response({
                    'success': False,
                    'error': 'OTP has expired. Please request a new one.',
                }, status=status.HTTP_400_BAD_REQUEST)

        # Check OTP match
        if contact.otp_code != otp_code:
            return Response({
                'success': False,
                'error': 'Invalid OTP code.',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Mark as verified
        contact.otp_verified = True
        contact.save(update_fields=['otp_verified'])

        # Generate signed token
        token = signing.dumps({
            'sl_name': sl_name,
            'contact_id': contact.id,
            'verified_at': timezone.now().isoformat(),
        })

        return Response({
            'success': True,
            'data': {
                'message': 'OTP verified successfully.',
                'token': token,
            }
        })


class SubmitContactView(APIView):
    """
    POST /api/v1/contact/submit/
    Accepts {token, topic, message}, validates token, saves message.
    """

    def post(self, request):
        serializer = SubmitContactSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'error': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['token']
        topic = serializer.validated_data['topic']
        message = serializer.validated_data['message']

        # Validate signed token
        try:
            data = signing.loads(token, max_age=TOKEN_EXPIRY_SECONDS)
        except signing.SignatureExpired:
            return Response({
                'success': False,
                'error': 'Verification token has expired. Please verify again.',
            }, status=status.HTTP_400_BAD_REQUEST)
        except signing.BadSignature:
            return Response({
                'success': False,
                'error': 'Invalid verification token.',
            }, status=status.HTTP_400_BAD_REQUEST)

        sl_name = data.get('sl_name')
        contact_id = data.get('contact_id')

        try:
            contact = ContactMessage.objects.get(
                id=contact_id,
                sl_name=sl_name,
                otp_verified=True,
                submitted_at__isnull=True,
            )
        except ContactMessage.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid or already used verification.',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save the message
        contact.topic = topic
        contact.message = message
        contact.submitted_at = timezone.now()
        contact.save(update_fields=['topic', 'message', 'submitted_at'])

        return Response({
            'success': True,
            'data': {
                'message': 'Your message has been submitted successfully. We will get back to you in-world!',
            }
        })
