"""
SL Bridge App — Views
Handles registration of the SL object URL and provides a utility
to push OTPs to the in-world LSL script.
"""
import logging

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SLObjectURL

logger = logging.getLogger(__name__)

# Timeout for outbound HTTP to the SL object (seconds)
SL_REQUEST_TIMEOUT = 10


class RegisterSLURLView(APIView):
    """
    POST /api/v1/sl-bridge/register-url/
    Called by the LSL script on region start / script reset to register
    the new dynamic object URL.

    Expected body:
        {
            "object_url": "http://simhost-xxxx.agni.secondlife.io:12046/cap/xxx",
            "secret": "<shared secret>"
        }
    """

    def post(self, request):
        secret = request.data.get('secret', '')
        object_url = request.data.get('object_url', '')

        # Validate shared secret
        expected_secret = getattr(settings, 'SL_BRIDGE_SECRET', '')
        if not expected_secret or secret != expected_secret:
            logger.warning("[SL Bridge] Registration rejected — invalid secret")
            return Response(
                {'success': False, 'error': 'Invalid secret.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not object_url:
            return Response(
                {'success': False, 'error': 'object_url is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deactivate all previous URLs
        SLObjectURL.objects.filter(is_active=True).update(is_active=False)

        # Register the new URL
        sl_url = SLObjectURL.objects.create(
            object_url=object_url,
            is_active=True,
        )

        logger.info(f"[SL Bridge] New SL object URL registered: {object_url[:80]}...")

        return Response({
            'success': True,
            'data': {
                'message': 'SL object URL registered successfully.',
                'id': sl_url.id,
            }
        })


def send_otp_to_sl(avatar_name: str, otp_code: str) -> bool:
    """
    Push an OTP to the in-world LSL object for delivery via llInstantMessage.

    Args:
        avatar_name: The SL username (e.g. "john.resident" or "FirstName LastName")
        otp_code: The 6-digit OTP code

    Returns:
        True if the OTP was successfully sent to the SL object, False otherwise.
    """
    sl_url_obj = SLObjectURL.get_active_url()

    if not sl_url_obj:
        logger.warning("[SL Bridge] No active SL object URL registered. OTP not delivered in-world.")
        return False

    secret = getattr(settings, 'SL_BRIDGE_SECRET', '')
    payload = f"secret={secret}&avatar_name={avatar_name}&otp_code={otp_code}"

    try:
        response = requests.post(
            sl_url_obj.object_url,
            data=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=SL_REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            logger.info(f"[SL Bridge] OTP delivered to SL object for '{avatar_name}'")
            return True
        else:
            logger.error(
                f"[SL Bridge] SL object returned status {response.status_code}: {response.text}"
            )
            # Mark URL as inactive if we get a connection-level failure
            if response.status_code in (404, 502, 503):
                sl_url_obj.is_active = False
                sl_url_obj.save(update_fields=['is_active'])
            return False

    except requests.exceptions.ConnectionError:
        logger.error("[SL Bridge] Could not connect to SL object — region may be down")
        sl_url_obj.is_active = False
        sl_url_obj.save(update_fields=['is_active'])
        return False
    except requests.exceptions.Timeout:
        logger.error("[SL Bridge] Request to SL object timed out")
        return False
    except Exception as e:
        logger.error(f"[SL Bridge] Unexpected error sending OTP to SL: {e}")
        return False
