"""
Contact App — Admin Configuration
"""
from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin for contact messages with read/unread management."""
    list_display = ['sl_name', 'topic', 'submitted_at', 'is_read', 'otp_verified']
    list_filter = ['is_read', 'topic', 'otp_verified', 'submitted_at']
    list_editable = ['is_read']
    search_fields = ['sl_name', 'message']
    readonly_fields = [
        'sl_name', 'topic', 'message', 'otp_code', 'otp_verified',
        'otp_created_at', 'submitted_at'
    ]
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} message(s) marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"

    def has_add_permission(self, request):
        # Contact messages should only come from the frontend
        return False
