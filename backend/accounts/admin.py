"""
Accounts App — Admin Customization
Customizes the Django admin site appearance for VASTIK.
"""
from django.contrib import admin

# Customize admin site
admin.site.site_header = "VASTIK Administration"
admin.site.site_title = "VASTIK Admin"
admin.site.index_title = "Dashboard"
