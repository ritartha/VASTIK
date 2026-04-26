"""
Management Command: load_sample_data
Creates sample products and gallery images for development/demo.

Usage:
    python manage.py load_sample_data
"""
import os
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image

from store.models import Product, ProductImage
from gallery.models import GalleryImage


def create_placeholder_image(width=800, height=600, color=(26, 18, 50), text="VASTIK"):
    """Generate a placeholder image with the VASTIK brand colors."""
    img = Image.new('RGB', (width, height), color)

    # Add a simple gradient-like effect using PIL
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)

    # Draw decorative border
    border_color = (245, 166, 35)  # Gold
    draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=2)
    draw.rectangle([20, 20, width-20, height-20], outline=(200, 134, 10), width=1)

    # Draw centered text
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except (IOError, OSError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), text, fill=(245, 166, 35), font=font)

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer


SAMPLE_PRODUCTS = [
    {
        'serial_number': 'VTK-001',
        'name': 'Mandala Temple Gate',
        'category': 'Mesh',
        'description': 'An intricately designed temple gate mesh with traditional Indian mandala patterns. '
                       'Perfect for creating authentic temple entrances in Second Life. '
                       'Includes LOD versions and land impact optimized geometry.',
        'price': 450,
        'marketplace_url': 'https://marketplace.secondlife.com/',
        'inworld_slurl': 'secondlife://VASTIK/128/128/25',
        'is_featured': True,
    },
    {
        'serial_number': 'VTK-002',
        'name': 'Rangoli Floor Set',
        'category': 'Mesh',
        'description': 'A beautiful collection of 6 rangoli floor designs with vibrant colors. '
                       'Each piece is sculpted with care and includes glow effects. '
                       'Low land impact, perfect for festivals and celebrations.',
        'price': 300,
        'marketplace_url': 'https://marketplace.secondlife.com/',
        'inworld_slurl': 'secondlife://VASTIK/128/128/25',
        'is_featured': False,
    },
    {
        'serial_number': 'VTK-003',
        'name': 'Smart Vendor Script',
        'category': 'Script',
        'description': 'An advanced vendor script with touch-to-buy, hover text pricing, '
                       'transaction logging, and automatic redelivery. '
                       'Includes a configuration notecard and full documentation.',
        'price': 200,
        'marketplace_url': 'https://marketplace.secondlife.com/',
        'inworld_slurl': 'secondlife://VASTIK/128/128/25',
        'is_featured': True,
    },
    {
        'serial_number': 'VTK-004',
        'name': 'Diya Particle Script',
        'category': 'Script',
        'description': 'A beautiful particle effect script that simulates traditional Indian diya (oil lamp) flames. '
                       'Configurable colors, intensity, and wind response. '
                       'Creates an authentic ambient atmosphere.',
        'price': 150,
        'marketplace_url': 'https://marketplace.secondlife.com/',
        'inworld_slurl': 'secondlife://VASTIK/128/128/25',
        'is_featured': False,
    },
    {
        'serial_number': 'VTK-005',
        'name': 'Silk Saree Fabric Pack',
        'category': 'Texture',
        'description': 'A premium pack of 12 high-resolution silk saree fabric textures. '
                       'Features traditional Indian patterns including Banarasi, Kanjeevaram, and Patola designs. '
                       'Full perm for clothing creators.',
        'price': 350,
        'marketplace_url': 'https://marketplace.secondlife.com/',
        'inworld_slurl': 'secondlife://VASTIK/128/128/25',
        'is_featured': True,
    },
    {
        'serial_number': 'VTK-006',
        'name': 'Henna Pattern Overlays',
        'category': 'Texture',
        'description': 'A collection of 8 seamless henna/mehndi pattern overlay textures. '
                       'Perfect for body tattoo layers, furniture decoration, or architectural detailing. '
                       'Includes alpha-masked and solid versions.',
        'price': 250,
        'marketplace_url': 'https://marketplace.secondlife.com/',
        'inworld_slurl': 'secondlife://VASTIK/128/128/25',
        'is_featured': False,
    },
]

SAMPLE_GALLERY = [
    'Temple Interior Showcase',
    'Festival of Lights Build',
    'Rangoli Art Exhibition',
    'Silk Market Scene',
]

# Color schemes per category for placeholder images
CATEGORY_COLORS = {
    'Mesh': (26, 18, 50),       # Deep indigo
    'Script': (50, 18, 26),     # Deep crimson
    'Texture': (50, 40, 10),    # Deep gold
}


class Command(BaseCommand):
    help = 'Load sample products and gallery images for VASTIK store'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Loading sample data for VASTIK...'))

        # Clear existing sample data
        Product.objects.filter(serial_number__startswith='VTK-').delete()
        GalleryImage.objects.filter(title__in=[g for g in SAMPLE_GALLERY]).delete()

        # Create products
        for product_data in SAMPLE_PRODUCTS:
            product = Product.objects.create(**product_data)

            # Create 2 placeholder images per product
            color = CATEGORY_COLORS.get(product_data['category'], (26, 18, 50))
            for i in range(2):
                img_text = f"{product_data['serial_number']}\n{product_data['name']}\nImage {i+1}"
                img_buffer = create_placeholder_image(
                    color=color,
                    text=img_text
                )
                image = ProductImage(product=product, order=i)
                image.image.save(
                    f"{product_data['serial_number'].lower()}_img{i+1}.png",
                    ContentFile(img_buffer.read()),
                    save=True,
                )

            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Created: {product_data['serial_number']} — {product_data['name']}")
            )

        # Create gallery images
        gallery_colors = [
            (30, 10, 50),   # Purple
            (50, 30, 10),   # Amber
            (10, 40, 40),   # Teal
            (50, 10, 20),   # Rose
        ]
        for idx, title in enumerate(SAMPLE_GALLERY):
            img_buffer = create_placeholder_image(
                width=1024,
                height=768,
                color=gallery_colors[idx % len(gallery_colors)],
                text=title
            )
            gallery_img = GalleryImage(title=title)
            gallery_img.image.save(
                f"gallery_{idx+1}.png",
                ContentFile(img_buffer.read()),
                save=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Gallery: {title}")
            )

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Loaded {len(SAMPLE_PRODUCTS)} products and {len(SAMPLE_GALLERY)} gallery images."
        ))
