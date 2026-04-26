"""
Store App — Admin Configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images."""
    model = ProductImage
    extra = 1
    fields = ['image', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 4px;" />',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Products."""
    list_display = [
        'serial_number', 'name', 'category', 'price_display',
        'is_featured', 'created_at'
    ]
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['serial_number', 'name', 'description']
    list_editable = ['is_featured']
    inlines = [ProductImageInline]

    def price_display(self, obj):
        return f"L${obj.price:,.0f}"
    price_display.short_description = "Price"
    price_display.admin_order_field = 'price'


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 4px;" />',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"
