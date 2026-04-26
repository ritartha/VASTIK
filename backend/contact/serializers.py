"""
Contact App — Serializers
"""
from rest_framework import serializers


class SendOTPSerializer(serializers.Serializer):
    """Validates the SL name for OTP generation."""
    sl_name = serializers.CharField(
        max_length=100,
        help_text="Second Life username"
    )

    def validate_sl_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("SL Name is required.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    """Validates SL name and OTP code for verification."""
    sl_name = serializers.CharField(max_length=100)
    otp_code = serializers.CharField(max_length=6, min_length=6)

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return value


class SubmitContactSerializer(serializers.Serializer):
    """Validates the full contact form submission with verified token."""
    token = serializers.CharField()
    topic = serializers.ChoiceField(choices=[
        ('Commission Work', 'Commission Work'),
        ('Product Related Issue', 'Product Related Issue'),
        ('Complaints', 'Complaints'),
        ('Suggestions', 'Suggestions'),
        ('Others', 'Others'),
    ])
    message = serializers.CharField(min_length=10)
