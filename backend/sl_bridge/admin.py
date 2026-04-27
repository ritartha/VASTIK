"""
SL Bridge App — Admin Configuration
"""
from django.contrib import admin
from .models import SLObjectURL


@admin.register(SLObjectURL)
class SLObjectURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_url', 'is_active', 'registered_at')
    list_filter = ('is_active',)
    readonly_fields = ('object_url', 'registered_at')
    ordering = ('-registered_at',)

    def short_url(self, obj):
        """Display a truncated URL for readability."""
        return obj.object_url[:80] + '...' if len(obj.object_url) > 80 else obj.object_url
    short_url.short_description = 'Object URL'
