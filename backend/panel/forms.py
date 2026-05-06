"""
Panel App — Forms
ModelForms for Product and image URL management.
"""
from django import forms
from store.models import Product, ProductImage


class ProductForm(forms.ModelForm):
    """Form for creating/editing a Product."""

    class Meta:
        model = Product
        fields = [
            'serial_number', 'name', 'category', 'description',
            'price', 'marketplace_url', 'inworld_slurl', 'is_featured',
        ]
        widgets = {
            'serial_number': forms.TextInput(attrs={
                'placeholder': 'e.g. VTK-001',
                'class': 'panel-input',
                'autocomplete': 'off',
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Product name',
                'class': 'panel-input',
            }),
            'category': forms.Select(attrs={
                'class': 'panel-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Product description...',
                'class': 'panel-input',
                'rows': 4,
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Price in L$',
                'class': 'panel-input',
                'min': 0,
            }),
            'marketplace_url': forms.URLInput(attrs={
                'placeholder': 'https://marketplace.secondlife.com/...',
                'class': 'panel-input',
            }),
            'inworld_slurl': forms.URLInput(attrs={
                'placeholder': 'secondlife://...',
                'class': 'panel-input',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'panel-checkbox',
            }),
        }


class ProductImageForm(forms.Form):
    """Form for a single product image URL entry."""

    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://example.com/image.jpg',
            'class': 'panel-input',
        }),
    )
    order = forms.IntegerField(
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': '0',
            'class': 'panel-input panel-input-sm',
            'min': 0,
        }),
    )
