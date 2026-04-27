"""
SL Bridge App — App Configuration
"""
from django.apps import AppConfig


class SlBridgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sl_bridge'
    verbose_name = 'Second Life Bridge'
